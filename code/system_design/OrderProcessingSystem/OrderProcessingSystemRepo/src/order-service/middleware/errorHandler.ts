import { Request, Response, NextFunction } from 'express';
import { logger } from '../../shared';

// Simple error handler for PoC
// Production would have more sophisticated error handling:
// - Error classification, user-friendly messages, error tracking (Sentry),
// - Different responses for different error types, etc.

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  logger.error('Unhandled error', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
  });

  // Don't expose internal errors in production
  const isDevelopment = process.env.NODE_ENV === 'development';
  
  res.status(500).json({
    error: 'Internal Server Error',
    message: isDevelopment ? error.message : 'Something went wrong',
    ...(isDevelopment && { stack: error.stack }),
  });
} 