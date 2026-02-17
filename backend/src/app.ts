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

    // Email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      console.log("❌ Validation failed: Invalid email format");
      return res.status(400).json({ error: "Invalid email format" });
    }

    const createData = {
      email,
      name,
      passwordHash: "temp123",
    };
    const user = await prisma.user.create({ data: createData });

    res.json(user);
  } catch (error: any) {
    res.status(400).json({ error: error.message });
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
