import { Router } from 'express'
import { WorkspaceController } from '../controllers/workspace.controller.js'
import { authMiddleware } from '../middleware/auth.middleware.js'
import { workspaceMiddleware } from '../middleware/workspace.middleware.js'
import { requireRole } from '../middleware/role.middleware.js'

const router = Router()

// List my workspaces (no workspace context needed - listing ALL user's workspaces)
router.get(
  '/',
  authMiddleware,  // Only needs: who are you?
  WorkspaceController.listMyWorkspaces
)

// All routes below need workspace context
// They all need to know: which workspace? are you member?

// List members in workspace
router.get(
  '/:id/members',
  authMiddleware,       // 1. Who are you?
  workspaceMiddleware,  // 2. Which workspace? Are you member?
  WorkspaceController.listMembers
)

// Change member role
router.patch(
  '/:id/members/:userId',
  authMiddleware,
  workspaceMiddleware,
  requireRole('OWNER', 'ADMIN'),  // 3. Do you have permission?
  WorkspaceController.changeMemberRole
)

// Remove member
router.delete(
  '/:id/members/:userId',
  authMiddleware,
  workspaceMiddleware,
  requireRole('OWNER', 'ADMIN'),
  WorkspaceController.removeMember
)

export default router
