import { Router, Request, Response } from 'express';
import { Database, redis, sqs } from '../../shared';

const router = Router();

// Simple health check for PoC
// Production would have more comprehensive health checks:
// - Database connection pool status, memory usage, CPU usage,
// - External service dependencies, custom business logic health checks

router.get('/', async (req: Request, res: Response) => {
  try {
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'order-service',
      version: process.env.npm_package_version || '1.0.0',
      uptime: process.uptime(),
      dependencies: {
        database: await Database.healthCheck(),
        redis: await redis.healthCheck(),
        sqs: await sqs.healthCheck(),
      },
    };

    // If any dependency is down, mark as unhealthy
    const allHealthy = Object.values(health.dependencies).every(Boolean);
    if (!allHealthy) {
      health.status = 'unhealthy';
      return res.status(503).json(health);
    }

    res.json(health);
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error instanceof Error ? error.message : 'Health check failed',
      timestamp: new Date().toISOString(),
    });
  }
});

// Liveness probe (for Kubernetes)
router.get('/live', (req: Request, res: Response) => {
  res.json({ status: 'alive' });
});

// Readiness probe (for Kubernetes)
router.get('/ready', async (req: Request, res: Response) => {
  try {
    const dbHealthy = await Database.healthCheck();
    if (dbHealthy) {
      res.json({ status: 'ready' });
    } else {
      res.status(503).json({ status: 'not ready' });
    }
  } catch (error) {
    res.status(503).json({ status: 'not ready' });
  }
});

export { router as healthRoutes }; 