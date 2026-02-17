import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { prisma } from "../lib/prisma.js";
import { redis } from "../lib/redis.js";

// Debug environment variables
console.log(
  "JWT_ACCESS_SECRET:",
  process.env.JWT_ACCESS_SECRET ? "✅ Loaded" : "❌ Missing",
);
console.log(
  "JWT_REFRESH_SECRET:",
  process.env.JWT_REFRESH_SECRET ? "✅ Loaded" : "❌ Missing",
);

export class AuthService {
  // Store refresh token in Redis (with fallback)
  static async storeRefreshToken(userId: string, refreshToken: string) {
    try {
      const key = `refresh_token:${userId}:${refreshToken}`;
      // Store for 7 days (same as token expiry)
      await redis.setex(key, 7 * 24 * 60 * 60, "1");
    } catch (error) {
      console.warn(
        "⚠️ Redis unavailable, skipping token storage:",
        error.message,
      );
      // Continue without Redis - tokens will still work but can't be blacklisted
    }
  }

  // Check if refresh token is valid (with fallback)
  static async isRefreshTokenValid(userId: string, refreshToken: string) {
    try {
      const key = `refresh_token:${userId}:${refreshToken}`;
      const exists = await redis.exists(key);
      return exists === 1;
    } catch (error) {
      console.warn(
        "⚠️ Redis unavailable, assuming token valid:",
        error.message,
      );
      // When Redis is unavailable, assume token is valid
      return true;
    }
  }

  // Blacklist refresh token (delete from Redis) (with fallback)
  static async blacklistRefreshToken(userId: string, refreshToken: string) {
    try {
      const key = `refresh_token:${userId}:${refreshToken}`;
      await redis.del(key);
    } catch (error) {
      console.warn(
        "⚠️ Redis unavailable, skipping token blacklisting:",
        error.message,
      );
      // Continue without Redis
    }
  }

  // Hash password
  static async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 12);
  }

  // Generate JWT tokens
  static generateTokens(userId: string, email: string) {
    const accessToken = jwt.sign(
      { userId, email },
      process.env.JWT_ACCESS_SECRET || "fallback-secret",
      { expiresIn: "15m" },
    );

    const refreshToken = jwt.sign(
      { userId, email },
      process.env.JWT_REFRESH_SECRET || "fallback-secret",
      { expiresIn: "7d" },
    );

    return { accessToken, refreshToken };
  }

  // Register new user
  static async register(email: string, password: string, name: string) {
    // 1. Check if email exists
    const existing = await prisma.user.findUnique({
      where: { email },
    });

    if (existing) {
      throw new Error("Email already registered");
    }

    // 2. Hash password
    const passwordHash = await this.hashPassword(password);

    // 3. Create user
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
      },
    });

    // 4. Generate tokens
    const tokens = this.generateTokens(user.id, user.email);

    // 5. Store refresh token in Redis
    await this.storeRefreshToken(user.id, tokens.refreshToken);

    // 6. Return user + tokens
    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      ...tokens,
    };
  }

  // Login user
  static async login(email: string, password: string) {
    // 1. Find user
    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      throw new Error("Invalid credentials");
    }

    // 2. Check password
    const isValid = await bcrypt.compare(password, user.passwordHash);

    if (!isValid) {
      throw new Error("Invalid credentials");
    }

    // 3. Generate tokens
    const tokens = this.generateTokens(user.id, user.email);

    // 4. Store refresh token in Redis
    await this.storeRefreshToken(user.id, tokens.refreshToken);

    // 5. Return
    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      ...tokens,
    };
  }

  // Refresh access token
  static async refreshAccessToken(refreshToken: string) {
    try {
      // 1. Verify refresh token signature
      const payload = jwt.verify(
        refreshToken,
        process.env.JWT_REFRESH_SECRET || "fallback-secret",
      ) as { userId: string; email: string };

      // 2. Check if token exists in Redis (not blacklisted)
      const isValid = await this.isRefreshTokenValid(
        payload.userId,
        refreshToken,
      );

      if (!isValid) {
        throw new Error("Invalid refresh token");
      }

      // 3. Generate new access token
      const accessToken = jwt.sign(
        { userId: payload.userId, email: payload.email },
        process.env.JWT_ACCESS_SECRET || "fallback-secret",
        { expiresIn: "15m" },
      );

      return { accessToken };
    } catch (error) {
      throw new Error("Invalid refresh token");
    }
  }

  // Logout
  static async logout(userId: string, refreshToken: string) {
    await this.blacklistRefreshToken(userId, refreshToken);
  }
}
