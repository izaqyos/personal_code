import type { NextFunction, Request, Response } from "express";
import { HttpError } from "../errors";
import { verifySession } from "../session";

export interface AuthUser {
  id: string;
  tenantId: string;
  roles: string[];
}

declare module "express-serve-static-core" {
  interface Request {
    user: AuthUser;
  }
}

export async function requireAuth(req: Request, _res: Response, next: NextFunction) {
  const token = req.header("authorization")?.replace(/^Bearer /, "");
  if (!token) return next(new HttpError(401, "unauthenticated"));
  try {
    req.user = await verifySession(token);
    next();
  } catch (e) {
    next(new HttpError(401, "unauthenticated"));
  }
}

export function requireRole(role: string) {
  return (req: Request, _res: Response, next: NextFunction) =>
    req.user?.roles.includes(role) ? next() : next(new HttpError(403, "forbidden"));
}
