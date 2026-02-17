import { Router } from "express";
import { WorkspaceController } from "../controllers/workspace.controller.js";
import { authMiddleware } from "../middleware/auth.middleware.js";
import { workspaceMiddleware } from "../middleware/workspace.middleware.js";
import { requireRole } from "../middleware/role.middleware.js";

const router = Router();

// List my workspaces (no workspace context needed)
router.get("/", authMiddleware, WorkspaceController.listMyWorkspaces);

// All routes below need workspace context
router.get(
  "/:id/members",
  authMiddleware,
  workspaceMiddleware,
  WorkspaceController.listMembers,
);

router.post(
  "/:id/invite",
  authMiddleware,
  workspaceMiddleware,
  requireRole("OWNER", "ADMIN"),
  WorkspaceController.inviteMember,
);

router.patch(
  "/:id/members/:userId",
  authMiddleware,
  workspaceMiddleware,
  requireRole("OWNER", "ADMIN"), // Only owner/admin can change roles
  WorkspaceController.changeMemberRole,
);

router.delete(
  "/:id/members/:userId",
  authMiddleware,
  workspaceMiddleware,
  requireRole("OWNER", "ADMIN"),
  WorkspaceController.removeMember,
);

export default router;
