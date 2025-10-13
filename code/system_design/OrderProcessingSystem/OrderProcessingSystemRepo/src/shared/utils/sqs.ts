import { SQSClient, SendMessageCommand, ReceiveMessageCommand, DeleteMessageCommand } from '@aws-sdk/client-sqs';
import { logger } from './logger';
import { v4 as uuidv4 } from 'uuid';

// Simple SQS client for PoC using ElasticMQ
// Production would use proper AWS credentials, error handling,
// dead letter queues, and batch processing

class SQSService {
  private client: SQSClient;
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.SQS_ENDPOINT || 'http://localhost:9324';
    
    // Configure for local ElasticMQ
    this.client = new SQSClient({
      region: process.env.AWS_REGION || 'us-east-1',
      endpoint: this.baseUrl,
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'x',
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'x',
      },
    });
  }

  private getQueueUrl(queueName: string): string {
    return `${this.baseUrl}/000000000000/${queueName}`;
  }

  // Publish message to FIFO queue
  // IMPORTANT: For global FIFO ordering, use same messageGroupId for all messages
  // This ensures strict chronological processing but limits throughput to 300 TPS
  async publishMessage(queueName: string, message: any, messageGroupId = 'default'): Promise<void> {
    const queueUrl = this.getQueueUrl(queueName);
    const messageBody = JSON.stringify(message);
    
    // Generate deduplication ID for FIFO queue
    const deduplicationId = uuidv4();

    try {
      const command = new SendMessageCommand({
        QueueUrl: queueUrl,
        MessageBody: messageBody,
        MessageGroupId: messageGroupId,
        MessageDeduplicationId: deduplicationId,
      });

      await this.client.send(command);
      logger.info('Message published to SQS', { 
        queue: queueName, 
        messageGroupId, 
        deduplicationId 
      });
    } catch (error) {
      logger.error('Failed to publish message to SQS', { 
        queue: queueName, 
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  // Poll for messages from FIFO queue
  async pollMessages(queueName: string, maxMessages = 1): Promise<any[]> {
    const queueUrl = this.getQueueUrl(queueName);

    try {
      const command = new ReceiveMessageCommand({
        QueueUrl: queueUrl,
        MaxNumberOfMessages: maxMessages,
        WaitTimeSeconds: 10, // Long polling
        VisibilityTimeout: 30,
      });

      const result = await this.client.send(command);
      const messages = result.Messages || [];

      logger.debug('Polled messages from SQS', { 
        queue: queueName, 
        messageCount: messages.length 
      });

      return messages.map(msg => ({
        body: JSON.parse(msg.Body || '{}'),
        receiptHandle: msg.ReceiptHandle,
        messageId: msg.MessageId,
      }));
    } catch (error) {
      logger.error('Failed to poll messages from SQS', { 
        queue: queueName, 
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  // Delete message after processing
  async deleteMessage(queueName: string, receiptHandle: string): Promise<void> {
    const queueUrl = this.getQueueUrl(queueName);

    try {
      const command = new DeleteMessageCommand({
        QueueUrl: queueUrl,
        ReceiptHandle: receiptHandle,
      });

      await this.client.send(command);
      logger.debug('Message deleted from SQS', { queue: queueName });
    } catch (error) {
      logger.error('Failed to delete message from SQS', { 
        queue: queueName, 
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      // Simple health check by trying to receive messages (but not wait)
      const queueUrl = this.getQueueUrl('orders-queue.fifo');
      const command = new ReceiveMessageCommand({
        QueueUrl: queueUrl,
        MaxNumberOfMessages: 1,
        WaitTimeSeconds: 0, // Don't wait for messages
      });
      await this.client.send(command);
      return true;
    } catch (error) {
      logger.error('SQS health check failed', { error });
      return false;
    }
  }
}

export const sqs = new SQSService(); 