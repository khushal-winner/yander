import type { Response } from "express";
import type { WorkspaceRequest } from "../middleware/workspace.middleware.js";
import type { AuthRequest } from "../middleware/auth.middleware.js";
import { prisma } from "../lib/prisma.js";
import crypto from "crypto";
import { sendInviteEmail } from "../lib/email.js";

export class WorkspaceController {
  // GET /api/workspaces
  // List all workspaces I'm a member of
  static async listMyWorkspaces(req: AuthRequest, res: Response) {
    try {
      const memberships = await prisma.workspaceMember.findMany({
        where: {
          userId: req.user!.userId,
        },
        include: {
          workspace: true,
        },
      });

      // Return workspaces with user's role in each
      const workspaces = memberships.map((m) => ({
        id: m.workspace.id,
        name: m.workspace.name,
        slug: m.workspace.slug,
        role: m.role,
        joinedAt: m.joinedAt,
      }));

      res.json(workspaces);
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  }

  // GET /api/workspaces/:id/members
  // List all members of a workspace
  static async listMembers(req: WorkspaceRequest, res: Response) {
    try {
      const members = await prisma.workspaceMember.findMany({
        where: {
          workspaceId: req.workspaceId,
        },
        include: {
          user: {
            select: {
              id: true,
              name: true,
              email: true,
              avatarUrl: true,
            },
          },
        },
      });

      res.json(members);
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  }

  // PATCH /api/workspaces/:id/members/:userId
  // Change member role
  static async changeMemberRole(req: WorkspaceRequest, res: Response) {
    try {
      const { userId } = req.params;
      const { role } = req.body;

      // Validate role
      const validRoles = ["ADMIN", "MEMBER", "VIEWER"];
      if (!validRoles.includes(role)) {
        return res.status(400).json({ error: "Invalid role" });
      }

      // Can't change owner's role
      const targetMember = await prisma.workspaceMember.findUnique({
        where: {
          workspaceId_userId: {
            workspaceId: req.workspaceId!,
            userId,
          },
        },
      });

      if (!targetMember) {
        return res.status(404).json({ error: "Member not found" });
      }

      if (targetMember.role === "OWNER") {
        return res.status(403).json({ error: "Can't change owner's role" });
      }

      const updated = await prisma.workspaceMember.update({
        where: {
          workspaceId_userId: {
            workspaceId: req.workspaceId!,
            userId,
          },
        },
        data: { role },
      });

      res.json(updated);
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  }

  // DELETE /api/workspaces/:id/members/:userId
  // Remove member from workspace
  static async removeMember(req: WorkspaceRequest, res: Response) {
    try {
      const { userId } = req.params;

      // Can't remove yourself (owner)
      if (userId === req.user!.userId && req.userRole === "OWNER") {
        return res.status(403).json({ error: "Owner cannot leave workspace" });
      }

      // Can't remove owner
      const targetMember = await prisma.workspaceMember.findUnique({
        where: {
          workspaceId_userId: {
            workspaceId: req.workspaceId!,
            userId,
          },
        },
      });

      if (targetMember?.role === "OWNER") {
        return res.status(403).json({ error: "Can't remove owner" });
      }

      await prisma.workspaceMember.delete({
        where: {
          workspaceId_userId: {
            workspaceId: req.workspaceId!,
            userId,
          },
        },
      });

      res.json({ message: "Member removed" });
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  }

  // POST /api/workspaces/:id/invite
  static async inviteMember(req: WorkspaceRequest, res: Response) {
    try {
      const { email, role = "MEMBER" } = req.body;

      if (!email) {
        return res.status(400).json({ error: "Email required" });
      }

      // Check if user already member
      const existingUser = await prisma.user.findUnique({ where: { email } });

      if (existingUser) {
        const alreadyMember = await prisma.workspaceMember.findUnique({
          where: {
            workspaceId_userId: {
              workspaceId: req.workspaceId!,
              userId: existingUser.id,
            },
          },
        });

        if (alreadyMember) {
          return res.status(400).json({ error: "User already a member" });
        }
      }

      // Generate secure random token
      const token = crypto.randomBytes(32).toString("hex");

      // Get inviter info
      const inviter = await prisma.user.findUnique({
        where: { id: req.user!.userId },
      });

      const workspace = await prisma.workspace.findUnique({
        where: { id: req.workspaceId },
      });

      // Create invitation
      const invitation = await prisma.invitation.create({
        data: {
          workspaceId: req.workspaceId!,
          email,
          role,
          token,
          invitedBy: req.user!.userId,
          expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        },
      });

      // Send email
      await sendInviteEmail(email, inviter!.name, workspace!.name, token);

      res.status(201).json({
        message: "Invitation sent",
        invitationId: invitation.id,
      });
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  }

  // POST /api/invitations/accept
  static async acceptInvitation(req: AuthRequest, res: Response) {
    try {
      const { token } = req.body;

      if (!token) {
        return res.status(400).json({ error: "Token required" });
      }

      // Find invitation
      const invitation = await prisma.invitation.findUnique({
        where: { token },
      });

      if (!invitation) {
        return res.status(404).json({ error: "Invitation not found" });
      }

      // Check not expired
      if (invitation.expiresAt < new Date()) {
        return res.status(400).json({ error: "Invitation expired" });
      }

      // Check not already accepted
      if (invitation.acceptedAt) {
        return res.status(400).json({ error: "Invitation already used" });
      }

      // Add user to workspace
      await prisma.$transaction(async (tx) => {
        // Add membership
        await tx.workspaceMember.create({
          data: {
            workspaceId: invitation.workspaceId,
            userId: req.user!.userId,
            role: invitation.role,
          },
        });

        // Mark invitation accepted
        await tx.invitation.update({
          where: { id: invitation.id },
          data: { acceptedAt: new Date() },
        });
      });

      res.json({
        message: "Joined workspace successfully",
        workspaceId: invitation.workspaceId,
      });
    } catch (error: any) {
      res.status(500).json({ error: error.message });
    }
  }
}
