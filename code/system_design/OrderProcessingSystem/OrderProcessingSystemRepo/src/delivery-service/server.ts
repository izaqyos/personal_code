import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { logger, Database } from '../shared';
import { deliveryRoutes } from './routes/delivery';
import { healthRoutes } from './routes/health';
import { errorHandler } from './middleware/errorHandler';
import { SQSConsumer } from './services/SQSConsumer';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.DELIVERY_SERVICE_PORT || 3002;

// Basic middleware for PoC
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

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
app.use('/delivery', deliveryRoutes);
app.use('/health', healthRoutes);

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Not Found', message: 'Endpoint not found' });
});

// Error handling middleware
app.use(errorHandler);

// SQS Consumer instance
const sqsConsumer = new SQSConsumer();

// Graceful shutdown
process.on('SIGINT', async () => {
  logger.info('Shutting down Delivery Service...');
  try {
    await sqsConsumer.stop();
    await Database.close();
    process.exit(0);
  } catch (error) {
    logger.error('Error during shutdown', { error });
    process.exit(1);
  }
});

// Start server and SQS consumer
async function startServer(): Promise<void> {
  try {
    // Start SQS consumer
    await sqsConsumer.start();
    
    app.listen(PORT, () => {
      logger.info('Delivery Service started', { 
        port: PORT, 
        env: process.env.NODE_ENV || 'development' 
      });
    });
  } catch (error) {
    logger.error('Failed to start Delivery Service', { error });
    process.exit(1);
  }
}

startServer(); 