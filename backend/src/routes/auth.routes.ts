import { Router } from "express";
import type { Response } from "express";
import { AuthService } from "../services/auth.service.js";
import {
  authMiddleware,
  type AuthRequest,
} from "../middleware/auth.middleware.js";

const router = Router();

// Register user
router.post("/register", async (req: AuthRequest, res: Response) => {
  try {
    const { email, password, name } = req.body;

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

// Login user
router.post("/login", async (req: AuthRequest, res: Response) => {
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

// Get current user
router.get("/me", authMiddleware, async (req: AuthRequest, res: Response) => {
  try {
    const { prisma } = await import("../lib/prisma.js");
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
  } catch (error: any) {
    res.status(401).json({ error: error.message });
  }
});

// Refresh token
router.post("/refresh", async (req: AuthRequest, res: Response) => {
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
router.post(
  "/logout",
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

export default router;
