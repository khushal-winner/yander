import type { Response, NextFunction } from "express";
import type { WorkspaceRequest } from "./workspace.middleware.js";

// Factory function that creates middleware for specific roles
export const requireRole = (...roles: string[]) => {
  return (req: WorkspaceRequest, res: Response, next: NextFunction) => {
    if (!req.userRole) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    if (!roles.includes(req.userRole)) {
      return res.status(403).json({
        error: `Requires role:${roles.join(" or ")}`,
      });
    }

    next();
  };
};

// Usage examples:
// requireRole('OWNER')            → Only owner
// requireRole('OWNER', 'ADMIN')   → Owner or admin
// requireRole('OWNER', 'ADMIN', 'MEMBER') → Anyone except viewer
