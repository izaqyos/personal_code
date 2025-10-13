import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { logger } from '../../shared';

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key-change-in-production';

// Simple JWT middleware for PoC
// Production would use Passport.js with proper strategies,
// token refresh, blacklisting, etc.

export interface AuthenticatedRequest extends Request {
  user?: {
    clientId: string;
    iat: number;
    exp: number;
  };
}

export function authenticateJWT(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): void {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({
      error: 'UNAUTHORIZED',
      message: 'Missing or invalid Authorization header',
    });
    return;
  }

  const token = authHeader.substring(7); // Remove 'Bearer ' prefix

  try {
    const decoded = jwt.verify(token, JWT_SECRET) as any;
    req.user = decoded;
    
    logger.debug('JWT authentication successful', { 
      clientId: decoded.clientId 
    });
    
    next();
  } catch (error) {
    logger.warn('JWT authentication failed', { 
      error: error instanceof Error ? error.message : error 
    });

    if (error instanceof jwt.TokenExpiredError) {
      res.status(401).json({
        error: 'TOKEN_EXPIRED',
        message: 'Access token has expired',
      });
      return;
    }

    if (error instanceof jwt.JsonWebTokenError) {
      res.status(401).json({
        error: 'INVALID_TOKEN',
        message: 'Invalid access token',
      });
      return;
    }

    res.status(401).json({
      error: 'UNAUTHORIZED',
      message: 'Token verification failed',
    });
  }
} 