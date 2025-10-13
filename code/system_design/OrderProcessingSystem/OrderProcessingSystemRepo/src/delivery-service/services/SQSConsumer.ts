import { sqs, logger } from '../../shared';
import { OrderCreatedEvent } from '../../shared';
import { DeliveryService } from './DeliveryService';

export class SQSConsumer {
  private isRunning = false;
  private deliveryService: DeliveryService;
  private pollingInterval?: NodeJS.Timeout;

  constructor() {
    this.deliveryService = new DeliveryService();
  }

  async start(): Promise<void> {
    if (this.isRunning) {
      logger.warn('SQS Consumer already running');
      return;
    }

    this.isRunning = true;
    logger.info('Starting SQS Consumer');

    // Start polling for messages
    this.pollingInterval = setInterval(async () => {
      await this.pollMessages();
    }, 5000); // Poll every 5 seconds

    // Initial poll
    await this.pollMessages();
  }

  async stop(): Promise<void> {
    if (!this.isRunning) {
      return;
    }

    this.isRunning = false;
    logger.info('Stopping SQS Consumer');

    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = undefined;
    }
  }

  private async pollMessages(): Promise<void> {
    if (!this.isRunning) {
      return;
    }

    try {
      const messages = await sqs.pollMessages('orders-queue.fifo', 10);
      
      if (messages.length === 0) {
        logger.debug('No messages received from SQS');
        return;
      }

      logger.info(`Processing ${messages.length} messages from SQS`);

      // Process messages sequentially to maintain order
      // Production would use parallel processing with careful ordering
      for (const message of messages) {
        try {
          // Add timeout to prevent hanging messages from blocking partition
          await this.processMessageWithTimeout(message, 30000); // 30-second timeout
          
          // Delete message after successful processing
          await sqs.deleteMessage('orders-queue.fifo', message.receiptHandle);
          
          logger.debug('Message processed and deleted', { 
            messageId: message.messageId 
          });
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : String(error);
          
          logger.error('Failed to process message', { 
            messageId: message.messageId,
            error: errorMessage,
            receiveCount: message.attributes?.ApproximateReceiveCount || '1'
          });
          
          // CRITICAL: Check retry count to prevent infinite blocking
          const receiveCount = parseInt(message.attributes?.ApproximateReceiveCount || '1');
          const maxRetries = 3;
          
          if (receiveCount >= maxRetries) {
            // After max retries, delete message to unblock partition
            // In production, this would be handled by SQS DLQ automatically
            logger.error('Message exceeded max retries, deleting to unblock partition', {
              messageId: message.messageId,
              receiveCount,
              maxRetries
            });
            
            try {
              await sqs.deleteMessage('orders-queue.fifo', message.receiptHandle);
              
              // TODO: Send to Dead Letter Queue for manual investigation
              await this.sendToDeadLetterQueue(message, errorMessage);
            } catch (deleteError) {
              logger.error('Failed to delete problematic message', {
                messageId: message.messageId,
                deleteError: deleteError instanceof Error ? deleteError.message : deleteError
              });
            }
          }
          // If under max retries, message will be retried automatically
        }
      }
    } catch (error) {
      logger.error('Error polling SQS messages', { 
        error: error instanceof Error ? error.message : error 
      });
    }
  }

  // Add timeout wrapper to prevent hanging messages
  private async processMessageWithTimeout(message: any, timeoutMs: number): Promise<void> {
    return new Promise(async (resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error(`Message processing timed out after ${timeoutMs}ms`));
      }, timeoutMs);

      try {
        await this.processMessage(message);
        clearTimeout(timeout);
        resolve();
      } catch (error) {
        clearTimeout(timeout);
        reject(error);
      }
    });
  }

  private async processMessage(message: any): Promise<void> {
    try {
      const event = message.body;
      
      if (!event.eventType) {
        logger.warn('Message missing eventType', { messageId: message.messageId });
        return;
      }

      logger.info('Processing event', { 
        eventType: event.eventType,
        messageId: message.messageId 
      });

      switch (event.eventType) {
        case 'ORDER_CREATED':
          await this.deliveryService.processOrderCreated(event as OrderCreatedEvent);
          break;
        
        default:
          logger.warn('Unknown event type', { 
            eventType: event.eventType,
            messageId: message.messageId 
          });
      }
    } catch (error) {
      logger.error('Error processing message', { 
        messageId: message.messageId,
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  // Handle messages that failed max retries to prevent partition blocking
  private async sendToDeadLetterQueue(message: any, errorReason: string): Promise<void> {
    try {
      const dlqMessage = {
        originalMessageId: message.messageId,
        originalBody: message.body,
        errorReason,
        failedAt: new Date().toISOString(),
        receiveCount: message.attributes?.ApproximateReceiveCount || 'unknown',
        // Store partition info for debugging
        partitionInfo: message.body?.eventType === 'ORDER_CREATED' ? {
          orderId: message.body?.orderId,
          customerId: message.body?.customerId,
          timestamp: message.body?.timestamp
        } : null
      };

      logger.warn('Sending failed message to DLQ for manual investigation', {
        originalMessageId: message.messageId,
        errorReason,
        orderId: dlqMessage.partitionInfo?.orderId
      });

      // In production, this would use actual SQS DLQ
      // For PoC, we log the DLQ message for manual handling
      logger.error('DEAD_LETTER_QUEUE_MESSAGE', dlqMessage);
      
      // TODO: In production, send to actual DLQ:
      // await sqs.publishMessage('orders-dlq.fifo', dlqMessage, 'dlq-partition');
      
    } catch (dlqError) {
      logger.error('Failed to send message to DLQ', {
        originalMessageId: message.messageId,
        dlqError: dlqError instanceof Error ? dlqError.message : dlqError
      });
    }
  }
} 