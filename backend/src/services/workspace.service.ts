import { prisma } from "../lib/prisma.js";
import { Role } from "@prisma/client";

export class WorkspaceService {
  // Get all workspaces a user is member of
  static async getUserWorkspaces(userId: string) {
    const memberships = await prisma.workspaceMember.findMany({
      where: {
        userId,
      },
      include: {
        workspace: true, // Include full workspace details
      },
      orderBy: {
        joinedAt: "desc", // Most recent first
      },
    });

    // Transform to cleaner format
    return memberships.map((m: any) => ({
      id: m.workspace.id,
      name: m.workspace.name,
      slug: m.workspace.slug,
      role: m.role,
      joinedAt: m.joinedAt,
      isOwner: m.role === "OWNER",
    }));
  }

  // Get all members of a workspace
  static async getWorkspaceMembers(workspaceId: string) {
    const members = await prisma.workspaceMember.findMany({
      where: {
        workspaceId,
      },
      include: {
        user: {
          select: {
            id: true,
            name: true,
            email: true,
            avatarUrl: true,
            createdAt: true,
          },
        },
      },
      orderBy: [
        { role: "asc" }, // OWNER first, then ADMIN, MEMBER, VIEWER
        { joinedAt: "asc" }, // Oldest members first within each role
      ],
    });

    return members.map((m: any) => ({
      id: m.id,
      role: m.role,
      joinedAt: m.joinedAt,
      user: m.user,
    }));
  }

  // Change member's role
  static async changeMemberRole(
    workspaceId: string,
    userId: string,
    newRole: Role,
  ) {
    // 1. Validate role is not OWNER (can't make someone else owner)
    if (newRole === "OWNER") {
      throw new Error("Cannot assign OWNER role");
    }

    // 2. Check target member exists and is not owner
    const targetMember = await prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId,
        },
      },
    });

    if (!targetMember) {
      throw new Error("Member not found");
    }

    if (targetMember.role === "OWNER") {
      throw new Error("Cannot change owner role");
    }

    // 3. Update role
    const updated = await prisma.workspaceMember.update({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId,
        },
      },
      data: {
        role: newRole,
      },
      include: {
        user: {
          select: {
            id: true,
            name: true,
            email: true,
          },
        },
      },
    });

    return updated;
  }

  // Remove member from workspace
  static async removeMember(
    workspaceId: string,
    userId: string,
    requestingUserId: string,
  ) {
    // 1. Get target member
    const targetMember = await prisma.workspaceMember.findUnique({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId,
        },
      },
    });

    if (!targetMember) {
      throw new Error("Member not found");
    }

    // 2. Prevent owner removal
    if (targetMember.role === "OWNER") {
      throw new Error("Cannot remove workspace owner");
    }

    // 3. Prevent self-removal if you're owner
    if (userId === requestingUserId && targetMember.role === "OWNER") {
      throw new Error("Owner cannot leave their own workspace");
    }

    // 4. Delete membership
    await prisma.workspaceMember.delete({
      where: {
        workspaceId_userId: {
          workspaceId,
          userId,
        },
      },
    });

    return { message: "Member removed successfully" };
  }
}
