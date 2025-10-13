import winston from 'winston';

// Simple logger setup for PoC
// Production would have more sophisticated logging with correlation IDs, 
// log aggregation (ELK stack), and different log levels per environment

const logLevel = process.env.LOG_LEVEL || 'info';

export const logger = winston.createLogger({
  level: logLevel,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { 
    service: process.env.SERVICE_NAME || 'order-processing' 
  },
  transports: [
    // Console output for development
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
    // Production would add file transport and external log aggregation
    // new winston.transports.File({ filename: 'error.log', level: 'error' }),
    // new winston.transports.File({ filename: 'combined.log' })
  ],
});

// Helper function to add correlation ID to logs
// Production would use proper correlation ID middleware
export const logWithCorrelation = (correlationId: string, level: string, message: string, meta?: any): void => {
  logger.log(level, message, { correlationId, ...meta });
}; 