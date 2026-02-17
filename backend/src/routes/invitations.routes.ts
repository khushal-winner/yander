import { Router } from 'express'
import { WorkspaceController } from '../controllers/workspace.controller.js'
import { authMiddleware } from '../middleware/auth.middleware.js'

const router = Router()

router.post('/accept', authMiddleware, WorkspaceController.acceptInvitation)

export default router
