import { Pool, PoolClient } from 'pg';
import { logger } from './logger';

// Simple database connection for PoC
// Production would use connection pooling (PgBouncer), read replicas,
// proper connection management, and database migrations

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'orderprocessing',
  user: process.env.DB_USER || 'admin',
  password: process.env.DB_PASSWORD || 'admin123',
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export class Database {
  static async query(text: string, params?: any[]): Promise<any> {
    const start = Date.now();
    try {
      const res = await pool.query(text, params);
      const duration = Date.now() - start;
      logger.debug('Database query executed', { 
        query: text, 
        duration, 
        rows: res.rowCount 
      });
      return res;
    } catch (error) {
      logger.error('Database query failed', { 
        query: text, 
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  static async getClient(): Promise<PoolClient> {
    return pool.connect();
  }

  static async transaction<T>(callback: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  static async close(): Promise<void> {
    await pool.end();
  }

  // Health check for monitoring
  static async healthCheck(): Promise<boolean> {
    try {
      await pool.query('SELECT 1');
      return true;
    } catch (error) {
      logger.error('Database health check failed', { error });
      return false;
    }
  }
} 