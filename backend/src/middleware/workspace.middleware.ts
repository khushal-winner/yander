import type { Request, Response, NextFunction } from "express";
import type { AuthRequest } from "./auth.middleware.js";
import { prisma } from "../lib/prisma.js";

// Extend request to include workspace info
export interface WorkspaceRequest extends AuthRequest, Request {
  workspaceId?: string;
  userRole?: string;
}

export const workspaceMiddleware = async (
  req: WorkspaceRequest,
  res: Response,
  next: NextFunction,
) => {
  try {
    // Get workspaceId from header
    // Frontend will send: 'x-workspace-id': 'uuid-here'
    const workspaceId = req.headers["x-workspace-id"] as string;

    if (!workspaceId) {
      return res.status(400).json({ error: "Workspace ID required" });
    }

    // Check user is member of this workspace
    const membership = await prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId: req.user!.userId,
        },
      },
      include: {
        workspace: true,
      },
    });

    if (!membership) {
      return res.status(403).json({ error: "Not a member of this workspace" });
    }

    // Attach to request for use in controllers
    req.workspaceId = workspaceId;
    req.userRole = membership.role;

    next();
  } catch (error) {
    res.status(500).json({ error: "Server error" });
  }
};
