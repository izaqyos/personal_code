# OAuth2 JWT Security Design

## Security Architecture Overview

Our system implements **OAuth2 with JWT tokens** using **Passport.js** middleware for authentication, providing enterprise-grade security with proper token lifecycle management.

## OAuth2 Flow Diagram

```mermaid
sequenceDiagram
    participant C as Customer/Client
    participant SA as Sales API
    participant AS as Auth Service
    participant DB as Auth Database
    
    Note over C,DB: OAuth2 JWT Authentication Flow
    
    %% Initial Authentication
    C->>AS: POST /auth/token (client_credentials)
    AS->>AS: Validate client credentials
    AS->>DB: Store refresh token
    AS->>AS: Generate JWT access token
    AS-->>C: {"access_token": "jwt...", "refresh_token": "...", "expires_in": 3600}
    
    %% API Request with Token
    C->>SA: POST /api/v1/orders (Authorization: Bearer jwt...)
    SA->>SA: Passport.js middleware validation
    SA->>SA: Verify JWT signature & expiration
    SA->>SA: Extract user/client info from token
    SA-->>C: Order response (if valid)
    
    %% Token Expiration & Refresh
    Note over C,AS: Token Refresh Flow
    C->>AS: POST /auth/refresh (refresh_token)
    AS->>DB: Validate refresh token
    AS->>AS: Generate new JWT access token
    AS->>DB: Update refresh token (optional rotation)
    AS-->>C: {"access_token": "new_jwt...", "expires_in": 3600}
```

## Security Components

### 1. Auth Service (New Component)
- **Responsibility**: OAuth2 token generation, validation, refresh
- **Technology**: Node.js/TypeScript with Passport.js
- **Port**: 3004
- **Key Features**:
  - Client credential management
  - JWT token generation/validation
  - Refresh token management
  - Rate limiting for auth endpoints

### 2. Enhanced Sales API Security
- **Passport.js Integration**: JWT strategy for token validation
- **Middleware Stack**: Authentication → Authorization → Rate Limiting
- **Protected Endpoints**: All `/api/v1/*` routes require valid JWT

## OAuth2 Endpoints

### Token Generation Endpoint

**POST /auth/token**
```json
Request:
{
  "grant_type": "client_credentials",
  "client_id": "sales_client_123",
  "client_secret": "secure_client_secret_456",
  "scope": "orders:create orders:read"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_abc123def456",
  "scope": "orders:create orders:read"
}

Error Response (400):
{
  "error": "invalid_client",
  "error_description": "Invalid client credentials"
}
```

### Token Refresh Endpoint

**POST /auth/refresh**
```json
Request:
{
  "grant_type": "refresh_token",
  "refresh_token": "refresh_abc123def456",
  "client_id": "sales_client_123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_new789ghi012", // Optional rotation
  "scope": "orders:create orders:read"
}
```

### Token Validation Endpoint

**GET /auth/validate**
```json
Request Headers:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Response (200):
{
  "valid": true,
  "client_id": "sales_client_123",
  "scope": ["orders:create", "orders:read"],
  "expires_at": "2024-01-15T15:30:00Z"
}

Response (401):
{
  "valid": false,
  "error": "token_expired",
  "error_description": "The access token has expired"
}
```

## JWT Token Structure

### JWT Header
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "auth-key-1"
}
```

### JWT Payload
```json
{
  "iss": "ecommerce-auth-service",
  "sub": "sales_client_123",
  "aud": "ecommerce-apis",
  "exp": 1642247400,
  "iat": 1642243800,
  "jti": "token-id-123",
  "scope": ["orders:create", "orders:read"],
  "client_type": "service",
  "rate_limit": {
    "requests_per_minute": 1000
  }
}
```

## Database Schema

### Auth Database Schema (PostgreSQL)

```sql
-- OAuth2 Clients table
CREATE TABLE oauth_clients (
    client_id VARCHAR(255) PRIMARY KEY,
    client_secret_hash VARCHAR(255) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    scopes TEXT[] NOT NULL DEFAULT '{}',
    rate_limit_rpm INTEGER DEFAULT 60,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Refresh Tokens table
CREATE TABLE refresh_tokens (
    token_id VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL REFERENCES oauth_clients(client_id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_revoked BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE
);

-- Token blacklist for revoked JWTs (before expiration)
CREATE TABLE jwt_blacklist (
    jti VARCHAR(255) PRIMARY KEY,
    client_id VARCHAR(255) NOT NULL,
    revoked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Rate limiting tracking
CREATE TABLE rate_limits (
    client_id VARCHAR(255) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    request_count INTEGER DEFAULT 0,
    window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (client_id, endpoint, window_start)
);

-- Indexes for performance
CREATE INDEX idx_refresh_tokens_client_id ON refresh_tokens(client_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
CREATE INDEX idx_jwt_blacklist_expires_at ON jwt_blacklist(expires_at);
CREATE INDEX idx_rate_limits_window ON rate_limits(client_id, endpoint, window_start);
```

## Implementation Examples

### Auth Service Implementation

```typescript
// services/auth-service/src/services/AuthService.ts
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import crypto from 'crypto';
import { PrismaClient } from '@prisma/client';

interface TokenRequest {
  grant_type: 'client_credentials' | 'refresh_token';
  client_id: string;
  client_secret?: string;
  refresh_token?: string;
  scope?: string;
}

interface TokenResponse {
  access_token: string;
  token_type: 'Bearer';
  expires_in: number;
  refresh_token: string;
  scope: string;
}

export class AuthService {
  private readonly jwtPrivateKey: string;
  private readonly jwtPublicKey: string;
  private readonly accessTokenTTL = 3600; // 1 hour
  private readonly refreshTokenTTL = 86400 * 30; // 30 days

  constructor(
    private prisma: PrismaClient,
    jwtPrivateKey: string,
    jwtPublicKey: string
  ) {
    this.jwtPrivateKey = jwtPrivateKey;
    this.jwtPublicKey = jwtPublicKey;
  }

  async generateToken(request: TokenRequest): Promise<TokenResponse> {
    if (request.grant_type === 'client_credentials') {
      return this.handleClientCredentialsGrant(request);
    } else if (request.grant_type === 'refresh_token') {
      return this.handleRefreshTokenGrant(request);
    } else {
      throw new Error('Unsupported grant type');
    }
  }

  private async handleClientCredentialsGrant(request: TokenRequest): Promise<TokenResponse> {
    // Validate client credentials
    const client = await this.validateClient(request.client_id, request.client_secret!);
    
    // Generate access token
    const accessToken = await this.createAccessToken(client);
    
    // Generate refresh token
    const refreshToken = await this.createRefreshToken(client.client_id);
    
    return {
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: this.accessTokenTTL,
      refresh_token: refreshToken,
      scope: client.scopes.join(' ')
    };
  }

  private async handleRefreshTokenGrant(request: TokenRequest): Promise<TokenResponse> {
    // Validate refresh token
    const tokenRecord = await this.validateRefreshToken(request.refresh_token!, request.client_id);
    
    // Get client info
    const client = await this.prisma.oauthClient.findUnique({
      where: { client_id: request.client_id }
    });

    if (!client || !client.is_active) {
      throw new Error('Invalid client');
    }

    // Generate new access token
    const accessToken = await this.createAccessToken(client);
    
    // Optionally rotate refresh token
    const newRefreshToken = await this.rotateRefreshToken(tokenRecord.token_id, client.client_id);
    
    return {
      access_token: accessToken,
      token_type: 'Bearer',
      expires_in: this.accessTokenTTL,
      refresh_token: newRefreshToken,
      scope: client.scopes.join(' ')
    };
  }

  private async createAccessToken(client: any): Promise<string> {
    const payload = {
      iss: 'ecommerce-auth-service',
      sub: client.client_id,
      aud: 'ecommerce-apis',
      exp: Math.floor(Date.now() / 1000) + this.accessTokenTTL,
      iat: Math.floor(Date.now() / 1000),
      jti: crypto.randomUUID(),
      scope: client.scopes,
      client_type: 'service',
      rate_limit: {
        requests_per_minute: client.rate_limit_rpm
      }
    };

    return jwt.sign(payload, this.jwtPrivateKey, { algorithm: 'RS256' });
  }

  private async createRefreshToken(clientId: string): Promise<string> {
    const tokenValue = crypto.randomBytes(32).toString('hex');
    const tokenHash = await bcrypt.hash(tokenValue, 12);
    
    await this.prisma.refreshToken.create({
      data: {
        token_id: crypto.randomUUID(),
        client_id: clientId,
        token_hash: tokenHash,
        expires_at: new Date(Date.now() + (this.refreshTokenTTL * 1000))
      }
    });

    return tokenValue;
  }

  private async validateClient(clientId: string, clientSecret: string): Promise<any> {
    const client = await this.prisma.oauthClient.findUnique({
      where: { client_id: clientId }
    });

    if (!client || !client.is_active) {
      throw new Error('Invalid client');
    }

    const isValidSecret = await bcrypt.compare(clientSecret, client.client_secret_hash);
    if (!isValidSecret) {
      throw new Error('Invalid client credentials');
    }

    return client;
  }

  async validateAccessToken(token: string): Promise<any> {
    try {
      const decoded = jwt.verify(token, this.jwtPublicKey, { algorithms: ['RS256'] });
      
      // Check if token is blacklisted
      const blacklisted = await this.prisma.jwtBlacklist.findUnique({
        where: { jti: (decoded as any).jti }
      });

      if (blacklisted) {
        throw new Error('Token has been revoked');
      }

      return decoded;
    } catch (error) {
      throw new Error('Invalid token');
    }
  }
}
```

### Passport.js Integration

```typescript
// services/sales-api/src/middleware/passport-config.ts
import passport from 'passport';
import { Strategy as JwtStrategy, ExtractJwt } from 'passport-jwt';
import { AuthService } from '../services/AuthService';

const authService = new AuthService(process.env.JWT_PUBLIC_KEY!);

passport.use(new JwtStrategy({
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_PUBLIC_KEY,
  algorithms: ['RS256'],
  issuer: 'ecommerce-auth-service',
  audience: 'ecommerce-apis'
}, async (payload, done) => {
  try {
    // Additional validation can be performed here
    // Check rate limits, permissions, etc.
    
    if (!payload.scope || !payload.scope.includes('orders:create')) {
      return done(null, false, { message: 'Insufficient scope' });
    }

    return done(null, {
      clientId: payload.sub,
      scopes: payload.scope,
      rateLimit: payload.rate_limit
    });
  } catch (error) {
    return done(error, false);
  }
}));

export default passport;
```

### Protected Route Implementation

```typescript
// services/sales-api/src/routes/orders.ts
import express from 'express';
import passport from '../middleware/passport-config';
import rateLimit from 'express-rate-limit';
import { OrderController } from '../controllers/OrderController';

const router = express.Router();

// Dynamic rate limiting based on JWT payload
const createRateLimiter = (req: any, res: any, next: any) => {
  const userRateLimit = req.user?.rateLimit?.requests_per_minute || 60;
  
  const limiter = rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: userRateLimit,
    keyGenerator: (req) => req.user?.clientId || req.ip,
    message: {
      error: 'rate_limit_exceeded',
      message: 'Too many requests'
    }
  });
  
  return limiter(req, res, next);
};

// Apply authentication middleware
router.use(passport.authenticate('jwt', { session: false }));

// Apply rate limiting
router.use(createRateLimiter);

// Protected routes
router.post('/orders', OrderController.createOrder);
router.get('/orders/:orderId', OrderController.getOrder);
router.put('/orders/:orderId/status', OrderController.updateOrderStatus);

export default router;
```

### Auth Controller

```typescript
// services/auth-service/src/controllers/AuthController.ts
import { Request, Response } from 'express';
import { AuthService } from '../services/AuthService';

export class AuthController {
  constructor(private authService: AuthService) {}

  async generateToken(req: Request, res: Response) {
    try {
      const tokenResponse = await this.authService.generateToken(req.body);
      res.json(tokenResponse);
    } catch (error) {
      res.status(400).json({
        error: 'invalid_request',
        error_description: error.message
      });
    }
  }

  async refreshToken(req: Request, res: Response) {
    try {
      const tokenResponse = await this.authService.generateToken({
        grant_type: 'refresh_token',
        ...req.body
      });
      res.json(tokenResponse);
    } catch (error) {
      res.status(400).json({
        error: 'invalid_grant',
        error_description: error.message
      });
    }
  }

  async validateToken(req: Request, res: Response) {
    try {
      const token = req.headers.authorization?.replace('Bearer ', '');
      if (!token) {
        return res.status(401).json({
          valid: false,
          error: 'missing_token'
        });
      }

      const decoded = await this.authService.validateAccessToken(token);
      res.json({
        valid: true,
        client_id: decoded.sub,
        scope: decoded.scope,
        expires_at: new Date(decoded.exp * 1000).toISOString()
      });
    } catch (error) {
      res.status(401).json({
        valid: false,
        error: 'invalid_token',
        error_description: error.message
      });
    }
  }

  async revokeToken(req: Request, res: Response) {
    try {
      const { token, token_type_hint } = req.body;
      
      if (token_type_hint === 'refresh_token') {
        await this.authService.revokeRefreshToken(token);
      } else {
        // Add JWT to blacklist
        await this.authService.blacklistJWT(token);
      }
      
      res.status(200).json({ message: 'Token revoked successfully' });
    } catch (error) {
      res.status(400).json({
        error: 'invalid_request',
        error_description: error.message
      });
    }
  }
}
```

## Security Configuration

### Environment Variables
```bash
# Auth Service
JWT_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----...
JWT_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----...
AUTH_DATABASE_URL=postgresql://auth_user:password@auth-db:5432/auth
BCRYPT_ROUNDS=12

# Sales API
JWT_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----...
AUTH_SERVICE_URL=http://auth-service:3004
```

### Docker Compose Updates
```yaml
version: '3.8'
services:
  # New Auth Service
  auth-service:
    build: ./services/auth-service
    ports: ["3004:3000"]
    environment:
      - DATABASE_URL=${AUTH_DB_URL}
      - JWT_PRIVATE_KEY=${JWT_PRIVATE_KEY}
      - JWT_PUBLIC_KEY=${JWT_PUBLIC_KEY}
      - NODE_ENV=development
    depends_on: [auth-db]
  
  # Updated Sales API
  sales-api:
    build: ./services/sales-api
    ports: ["3001:3000"]
    environment:
      - DATABASE_URL=${SALES_DB_URL}
      - REDIS_URL=${REDIS_URL}
      - PRODUCT_SERVICE_URL=http://product-service:3000
      - AUTH_SERVICE_URL=http://auth-service:3000
      - JWT_PUBLIC_KEY=${JWT_PUBLIC_KEY}
      - NODE_ENV=development
    depends_on: [sales-db, redis, product-service, auth-service]
  
  # New Auth Database
  auth-db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=auth
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes: ["auth_data:/var/lib/postgresql/data"]

volumes:
  auth_data:
```

## Security Benefits

### 🔒 **Enhanced Security Features**
- **RSA-256 JWT Signatures**: Cryptographically secure tokens
- **Refresh Token Rotation**: Prevents token replay attacks
- **Token Blacklisting**: Immediate revocation capability
- **Rate Limiting**: Per-client configurable limits
- **Scope-based Authorization**: Fine-grained permissions

### 🛡️ **Attack Mitigation**
- **Token Theft**: Short-lived access tokens with refresh mechanism
- **Replay Attacks**: JTI (JWT ID) tracking and blacklisting
- **Brute Force**: Rate limiting and account lockout
- **Privilege Escalation**: Scope validation for each request

### 📊 **Performance Considerations**
- **Time Complexity**: O(1) for JWT validation (local verification)
- **Space Complexity**: O(n) for blacklist storage where n = revoked tokens
- **Database Load**: Minimal - only for refresh token validation
- **Cache Strategy**: JWT public key caching for faster validation

This OAuth2 JWT implementation provides enterprise-grade security with proper token lifecycle management, meeting modern security standards for API authentication! 🔐 