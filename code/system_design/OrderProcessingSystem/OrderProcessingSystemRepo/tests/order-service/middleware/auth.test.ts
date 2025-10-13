import { expect } from 'chai';
import sinon from 'sinon';
import jwt from 'jsonwebtoken';
import { Request, Response } from 'express';
import { authenticateJWT, AuthenticatedRequest } from '../../../src/order-service/middleware/auth';

describe('JWT Authentication Middleware', () => {
  let req: Partial<AuthenticatedRequest>;
  let res: any;
  let next: sinon.SinonSpy;
  let jwtVerifyStub: sinon.SinonStub;

  beforeEach(() => {
    req = {
      headers: {}
    };
    res = {
      status: sinon.stub().returnsThis(),
      json: sinon.stub()
    };
    next = sinon.spy();
    jwtVerifyStub = sinon.stub(jwt, 'verify');
  });

  afterEach(() => {
    sinon.restore();
  });

  describe('authenticateJWT', () => {
    it('should authenticate valid JWT token', () => {
      // Arrange
      const mockPayload = {
        clientId: 'test-client',
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + 3600
      };

      req.headers = {
        authorization: 'Bearer valid-token'
      };

      jwtVerifyStub.returns(mockPayload);

      // Act
      authenticateJWT(req as AuthenticatedRequest, res as Response, next);

      // Assert
      expect(req.user).to.deep.equal(mockPayload);
      expect(next.calledOnce).to.be.true;
      expect(res.status.called).to.be.false;
    });

    it('should reject request without authorization header', () => {
      // Arrange
      req.headers = {};

      // Act
      authenticateJWT(req as AuthenticatedRequest, res as Response, next);

      // Assert
      expect(res.status.calledWith(401)).to.be.true;
      expect(res.json.calledWith({
        error: 'UNAUTHORIZED',
        message: 'Missing or invalid Authorization header'
      })).to.be.true;
      expect(next.called).to.be.false;
    });

    it('should reject request with invalid authorization header format', () => {
      // Arrange
      req.headers = {
        authorization: 'InvalidFormat token'
      };

      // Act
      authenticateJWT(req as AuthenticatedRequest, res as Response, next);

      // Assert
      expect(res.status.calledWith(401)).to.be.true;
      expect(res.json.calledWith({
        error: 'UNAUTHORIZED',
        message: 'Missing or invalid Authorization header'
      })).to.be.true;
      expect(next.called).to.be.false;
    });

    it('should handle expired token', () => {
      // Arrange
      req.headers = {
        authorization: 'Bearer expired-token'
      };

      jwtVerifyStub.throws(new jwt.TokenExpiredError('Token expired', new Date()));

      // Act
      // Note: Warning logs below are expected for this test scenario
      authenticateJWT(req as AuthenticatedRequest, res as Response, next);

      // Assert
      expect(res.status.calledWith(401)).to.be.true;
      expect(res.json.calledWith({
        error: 'TOKEN_EXPIRED',
        message: 'Access token has expired'
      })).to.be.true;
      expect(next.called).to.be.false;
    });

    it('should handle invalid token', () => {
      // Arrange
      req.headers = {
        authorization: 'Bearer invalid-token'
      };

      jwtVerifyStub.throws(new jwt.JsonWebTokenError('Invalid token'));

      // Act
      // Note: Warning logs below are expected for this test scenario
      authenticateJWT(req as AuthenticatedRequest, res as Response, next);

      // Assert
      expect(res.status.calledWith(401)).to.be.true;
      expect(res.json.calledWith({
        error: 'INVALID_TOKEN',
        message: 'Invalid access token'
      })).to.be.true;
      expect(next.called).to.be.false;
    });

    it('should handle generic JWT verification error', () => {
      // Arrange
      req.headers = {
        authorization: 'Bearer some-token'
      };

      jwtVerifyStub.throws(new Error('Generic JWT error'));

      // Act
      // Note: Warning logs below are expected for this test scenario
      authenticateJWT(req as AuthenticatedRequest, res as Response, next);

      // Assert
      expect(res.status.calledWith(401)).to.be.true;
      expect(res.json.calledWith({
        error: 'UNAUTHORIZED',
        message: 'Token verification failed'
      })).to.be.true;
      expect(next.called).to.be.false;
    });
  });
}); 