import { Router, Request, Response } from 'express';
import jwt, { SignOptions } from 'jsonwebtoken';
import { logger } from '../../shared';

const router = Router();

// Simple JWT auth for PoC
// Production would have:
// - Proper OAuth2 server, client registration, scopes,
// - Refresh tokens, token rotation, user authentication,
// - Rate limiting, brute force protection

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-key-change-in-production';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';

interface TokenRequest {
  client_id?: string;
  client_secret?: string;
  grant_type?: string;
}

// OAuth2 Client Credentials Flow (simplified)
router.post('/token', (req: Request, res: Response) => {
  try {
    const { client_id, client_secret, grant_type }: TokenRequest = req.body;

    // Basic validation for PoC
    // Production would validate against registered clients
    if (!client_id || !client_secret || grant_type !== 'client_credentials') {
      return res.status(400).json({
        error: 'invalid_request',
        error_description: 'Missing or invalid parameters',
      });
    }

    // Simple client validation for PoC
    // Production would check against database of registered clients
    const validClients = ['demo-client', 'test-client', 'order-app'];
    if (!validClients.includes(client_id) || client_secret !== 'demo-secret') {
      return res.status(401).json({
        error: 'invalid_client',
        error_description: 'Invalid client credentials',
      });
    }

    // Generate JWT token
    const payload = {
      clientId: client_id,
    };

    const options: SignOptions = { 
      expiresIn: '24h',
      issuer: 'order-processing-system',
      audience: 'order-api',
    };
    const token = jwt.sign(payload, JWT_SECRET, options);

    logger.info('JWT token issued', { clientId: client_id });

    res.json({
      access_token: token,
      token_type: 'Bearer',
      expires_in: 86400, // 24 hours in seconds
      scope: 'order:create order:read',
    });
  } catch (error) {
    logger.error('Token generation failed', { error });
    res.status(500).json({
      error: 'server_error',
      error_description: 'Token generation failed',
    });
  }
});

// Token introspection endpoint (for debugging)
router.post('/introspect', (req: Request, res: Response) => {
  try {
    const { token } = req.body;
    
    if (!token) {
      return res.status(400).json({ error: 'Missing token' });
    }

    const decoded = jwt.verify(token, JWT_SECRET) as any;
    
    res.json({
      active: true,
      client_id: decoded.clientId,
      exp: decoded.exp,
      iat: decoded.iat,
      scope: 'order:create order:read',
    });
  } catch (error) {
    res.json({
      active: false,
    });
  }
});

export { router as authRoutes }; 