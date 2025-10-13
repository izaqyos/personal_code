import { createClient, RedisClientType } from 'redis';
import { logger } from './logger';
import crypto from 'crypto';

// Simple Redis client for PoC idempotency
// Production would have Redis cluster, sentinel for HA, 
// proper error handling, and connection pooling

class RedisClient {
  private client: RedisClientType | null = null;

  async connect(): Promise<void> {
    if (this.client) return;

    this.client = createClient({
      socket: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT || '6379'),
      },
      password: process.env.REDIS_PASSWORD || undefined,
    });

    this.client.on('error', (err) => {
      logger.error('Redis Client Error', { error: err.message });
    });

    await this.client.connect();
    logger.info('Connected to Redis');
  }

  async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.disconnect();
      this.client = null;
    }
  }

  // Generate fingerprint for idempotency
  generateFingerprint(customerId: string, items: any[]): string {
    // Create deterministic fingerprint based ONLY on business data
    // Sort items to ensure consistent ordering
    const sortedItems = items
      .map(item => `${item.product_id}:${item.quantity}:${item.unit_price}`)
      .sort()
      .join('|');
    
    const data = `${customerId}:${sortedItems}`;
    return crypto.createHash('sha256').update(data).digest('hex').substring(0, 32);
  }

  // Check if request was already processed (idempotency)
  async checkIdempotency(fingerprint: string): Promise<string | null> {
    if (!this.client) throw new Error('Redis not connected');
    
    const key = `order:create:${fingerprint}`;
    try {
      const result = await this.client.get(key);
      if (result) {
        logger.info('Idempotent request detected', { fingerprint });
      }
      return result;
    } catch (error) {
      logger.error('Redis get failed', { error, key });
      // Don't fail the request if Redis is down - just proceed without idempotency
      return null;
    }
  }

  // Store result for idempotency
  async storeIdempotencyResult(fingerprint: string, result: any, ttlSeconds = 86400): Promise<void> {
    if (!this.client) throw new Error('Redis not connected');
    
    const key = `order:create:${fingerprint}`;
    try {
      await this.client.setEx(key, ttlSeconds, JSON.stringify(result));
      logger.debug('Stored idempotency result', { fingerprint, ttl: ttlSeconds });
    } catch (error) {
      logger.error('Redis setEx failed', { error, key });
      // Don't fail the request if Redis is down
    }
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    if (!this.client) return false;
    try {
      await this.client.ping();
      return true;
    } catch (error) {
      logger.error('Redis health check failed', { error });
      return false;
    }
  }
}

export const redis = new RedisClient(); 