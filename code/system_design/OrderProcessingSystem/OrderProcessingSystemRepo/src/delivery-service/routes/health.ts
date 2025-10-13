import { Router, Request, Response } from 'express';
import { Database, sqs } from '../../shared';

const router = Router();

router.get('/', async (req: Request, res: Response) => {
  try {
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'delivery-service',
      version: process.env.npm_package_version || '1.0.0',
      uptime: process.uptime(),
      dependencies: {
        database: await Database.healthCheck(),
        sqs: await sqs.healthCheck(),
      },
    };

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

router.get('/live', (req: Request, res: Response) => {
  res.json({ status: 'alive' });
});

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