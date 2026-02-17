import type { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

interface TokenPayload {
  userId: string;
  email: string;
}

// Extend Express Request to include user
export interface AuthRequest extends Request {
  user?: TokenPayload;
}

export const authMiddleware = (
  req: AuthRequest,
  res: Response,
  next: NextFunction,
) => {
  try {
    // 1. Get token from header
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ error: "No token provided" });
    }

    // 2. Extract token
    const token = authHeader.substring(7); // Remove 'Bearer '

    // 3. Verify token
    const payload = jwt.verify(
      token,
      process.env.JWT_ACCESS_SECRET || "fallback-secret",
    ) as TokenPayload;

    // 4. Attach user to request
    req.user = payload;

    // 5. Continue to route
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
};
