import type { Response } from "express";
import type { WorkspaceRequest } from "../middleware/workspace.middleware.js";
import type { AuthRequest } from "../middleware/auth.middleware.js";
import { WorkspaceService } from "../services/workspace.service.js";
import { Role } from "@prisma/client";

export class WorkspaceController {
  // GET /api/workspaces
  // List all workspaces I'm a member of
  static async listMyWorkspaces(req: AuthRequest, res: Response) {
    try {
      const workspaces = await WorkspaceService.getUserWorkspaces(
        req.user!.userId,
      );

      res.json(workspaces);
    } catch (error: any) {
      console.error("List workspaces error:", error);
      res.status(500).json({ error: error.message });
    }
  }

  // GET /api/workspaces/:id/members
  // List all members in a workspace
  static async listMembers(req: WorkspaceRequest, res: Response) {
    try {
      // workspaceId comes from middleware
      const members = await WorkspaceService.getWorkspaceMembers(
        req.workspaceId!,
      );

      res.json(members);
    } catch (error: any) {
      console.error("List members error:", error);
      res.status(500).json({ error: error.message });
    }
  }

  // PATCH /api/workspaces/:id/members/:userId
  // Change a member's role
  static async changeMemberRole(req: WorkspaceRequest, res: Response) {
    try {
      const { userId } = req.params;
      const { role } = req.body;

      // 1. Validate userId exists
      if (!userId || typeof userId !== "string") {
        return res.status(400).json({
          error: "Valid userId is required",
        });
      }

      // 2. Validate role value
      const validRoles: Role[] = ["ADMIN", "MEMBER", "VIEWER"];
      if (!validRoles.includes(role as Role)) {
        return res.status(400).json({
          error: "Invalid role. Must be ADMIN, MEMBER, or VIEWER",
        });
      }

      // 3. Change role (service handles business logic)
      const updated = await WorkspaceService.changeMemberRole(
        req.workspaceId!,
        userId,
        role as Role,
      );

      res.json(updated);
    } catch (error: any) {
      console.error("Change role error:", error);

      // Handle specific errors
      if (error.message.includes("not found")) {
        return res.status(404).json({ error: error.message });
      }
      if (error.message.includes("Cannot")) {
        return res.status(403).json({ error: error.message });
      }

      res.status(500).json({ error: error.message });
    }
  }

  // DELETE /api/workspaces/:id/members/:userId
  // Remove member from workspace
  static async removeMember(req: WorkspaceRequest, res: Response) {
    try {
      const { userId } = req.params;

      // 1. Validate userId exists
      if (!userId || typeof userId !== "string") {
        return res.status(400).json({
          error: "Valid userId is required",
        });
      }

      await WorkspaceService.removeMember(
        req.workspaceId!,
        userId,
        req.user!.userId, // Who's requesting this
      );

      res.json({ message: "Member removed successfully" });
    } catch (error: any) {
      console.error("Remove member error:", error);

      if (error.message.includes("not found")) {
        return res.status(404).json({ error: error.message });
      }
      if (error.message.includes("Cannot")) {
        return res.status(403).json({ error: error.message });
      }

      res.status(500).json({ error: error.message });
    }
  }
}
