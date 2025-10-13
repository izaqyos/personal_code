import { Request, Response, NextFunction } from 'express';
import { logger } from '../../shared';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  logger.error('Unhandled error in Delivery Service', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
  });

  const isDevelopment = process.env.NODE_ENV === 'development';
  
  res.status(500).json({
    error: 'Internal Server Error',
    message: isDevelopment ? error.message : 'Something went wrong',
    ...(isDevelopment && { stack: error.stack }),
  });
} 