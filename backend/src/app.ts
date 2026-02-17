import dotenv from "dotenv";
dotenv.config();

import express from "express";
import type { Request, Response, NextFunction } from "express";
import cors from "cors";
import { prisma } from "./lib/prisma.js";
import { AuthService } from "./services/auth.service.js";
import {
  authMiddleware,
  type AuthRequest,
} from "./middleware/auth.middleware.js";
import { redis } from "./lib/redis.js";
import workspaceRoutes from "./routes/workspace.routes.js";
import invitationsRoutes from "./routes/invitations.routes.js";

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors({ origin: "http://localhost:3000", credentials: true }));
app.use(express.json());

app.get("/", (req: Request, res: Response) => {
  console.log("✅ Root endpoint hit");
  res.json({ message: "Hello World" });
});

app.post("/users", async (req: Request, res: Response) => {
  try {
    const { email, name } = req.body;

    if (!email || !name) {
      console.log("❌ Validation failed: Missing email or name");
      return res.status(400).json({ error: "Email and name are required" });
    }

    const createData = {
      email,
      name,
      passwordHash: "temp123",
    };
    const user = await prisma.user.create({ data: createData });

    res.json(user);
  } catch (error: any) {
    console.error("❌ User creation error:", error.message);

    // Check if it's a unique constraint error
    if (error.message.includes("Unique constraint failed")) {
      return res.status(400).json({ error: error.message });
    }

    // Check if it's a database connection error
    if (error.message.includes("Database connection failed")) {
      return res.status(500).json({ error: "Database connection failed" });
    }

    // Generic error
    res.status(500).json({ error: error.message });
  }
});

app.delete("/users/:id", async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const deletedUser = await prisma.user.delete({ where: { id } });

    if (!deletedUser) {
      return res.status(404).json({ error: "User not found" });
    }

    res.status(204).send();
  } catch (error: any) {
    console.error("❌ User deletion error:", error.message);
    res.status(500).json({ error: error.message });
  }
});

app.post("/auth/register", async (req: Request, res: Response) => {
  try {
    const { email, password, name } = req.body;

    // Validation
    if (!email || !password || !name) {
      return res.status(400).json({ error: "Missing fields" });
    }

    if (password.length < 8) {
      return res.status(400).json({ error: "Password too short" });
    }

    const result = await AuthService.register(email, password, name);
    res.status(201).json(result);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
  }
});

app.post("/auth/login", async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: "Missing fields" });
    }

    const result = await AuthService.login(email, password);
    res.json(result);
  } catch (error: any) {
    res.status(401).json({ error: error.message });
  }
});

app.get("/auth/me", authMiddleware, async (req: AuthRequest, res: Response) => {
  // req.user is available because middleware verified it!
  const user = await prisma.user.findUnique({
    where: { id: req.user!.userId },
    select: {
      id: true,
      email: true,
      name: true,
      createdAt: true,
    },
  });

  res.json(user);
});

// Refresh token
app.post("/auth/refresh", async (req: Request, res: Response) => {
  try {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      return res.status(400).json({ error: "Refresh token required" });
    }

    const result = await AuthService.refreshAccessToken(refreshToken);
    res.json(result);
  } catch (error: any) {
    res.status(401).json({ error: error.message });
  }
});

// Logout
app.post(
  "/auth/logout",
  authMiddleware,
  async (req: AuthRequest, res: Response) => {
    try {
      const { refreshToken } = req.body;

      if (!refreshToken) {
        return res.status(400).json({ error: "Refresh token required" });
      }

      await AuthService.logout(req.user!.userId, refreshToken);
      res.json({ message: "Logged out successfully" });
    } catch (error: any) {
      res.status(400).json({ error: error.message });
    }
  },
);

app.get("/test-redis", async (req: Request, res: Response) => {
  try {
    await redis.set("test", "hello");
    const value = await redis.get("test");
    res.json({ value });
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

app.get("/error", (req: Request, res: Response) => {
  throw new Error("Something broke!");
});

// Global error handler
app.use((error: any, req: Request, res: Response, next: NextFunction) => {
  console.error("❌ Global error handler:", error);
  res.status(500).json({ error: "Something broke!" });
});

// Workspace routes
app.use("/api/workspaces", workspaceRoutes);

// Invitation routes
app.use("/api/invitations", invitationsRoutes);

async function startServer() {
  try {
    // Connect to Redis
    await redis.connect();
    console.log("✅ Redis connected and ready");

    app.listen(PORT, () => {
      console.log(`🚀 Server running on http://localhost:${PORT}`);
    });
  } catch (error) {
    console.error("❌ Failed to connect to Redis:", error);
    console.log("⚠️ Starting server without Redis (caching will be disabled)");

    app.listen(PORT, () => {
      console.log(
        `🚀 Server running on http://localhost:${PORT} (Redis unavailable)`,
      );
    });
  }
}

startServer();
