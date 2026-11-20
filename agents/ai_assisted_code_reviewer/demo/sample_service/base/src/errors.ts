import type { NextFunction, Request, Response } from "express";
import { logger } from "./logger";

export class HttpError extends Error {
  constructor(public status: number, message: string, public code = "error") {
    super(message);
  }
}

export function errorHandler(err: unknown, req: Request, res: Response, _next: NextFunction) {
  const status = err instanceof HttpError ? err.status : 500;
  const message = err instanceof HttpError ? err.message : "internal error";
  if (status >= 500) logger.error("unhandled error", { err, path: req.path });
  res.status(status).json({ error: { code: err instanceof HttpError ? err.code : "internal", message } });
}
