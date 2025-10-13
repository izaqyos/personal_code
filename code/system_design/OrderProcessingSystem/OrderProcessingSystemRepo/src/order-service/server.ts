import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { logger, Database, redis } from '../shared';
import { authRoutes } from './routes/auth';
import { orderRoutes } from './routes/orders';
import { healthRoutes } from './routes/health';
import { errorHandler } from './middleware/errorHandler';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.ORDER_SERVICE_PORT || 3001;

// Basic middleware for PoC
// Production would have more sophisticated middleware:
// - Rate limiting, request validation, CORS configuration,
// - Request ID generation, API versioning, etc.
app.use(helmet()); // Basic security headers
app.use(cors()); // Allow cross-origin requests
app.use(express.json({ limit: '10mb' })); // Parse JSON bodies

// Request logging middleware
app.use((req, res, next) => {
  logger.info('HTTP Request', {
    method: req.method,
    url: req.url,
    userAgent: req.get('User-Agent'),
    ip: req.ip,
  });
  next();
});

// Routes
app.use('/auth', authRoutes);
app.use('/orders', orderRoutes);
app.use('/health', healthRoutes);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Not Found', message: 'Endpoint not found' });
});

// Error handling middleware
app.use(errorHandler);

// Graceful shutdown
process.on('SIGINT', async () => {
  logger.info('Shutting down Order Service...');
  try {
    await Database.close();
    await redis.disconnect();
    process.exit(0);
  } catch (error) {
    logger.error('Error during shutdown', { error });
    process.exit(1);
  }
});

// Start server
async function startServer(): Promise<void> {
  try {
    // Connect to Redis for idempotency
    await redis.connect();
    
    app.listen(PORT, () => {
      logger.info('Order Service started', { 
        port: PORT, 
        env: process.env.NODE_ENV || 'development' 
      });
    });
  } catch (error) {
    logger.error('Failed to start Order Service', { error });
    process.exit(1);
  }
}

startServer(); 