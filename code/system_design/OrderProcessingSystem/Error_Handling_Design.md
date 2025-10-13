# Error Handling Design: Circuit Breakers & Retry Mechanisms

## Overview

This document defines comprehensive error handling strategies for our microservices architecture, using proven npm libraries: `opossum` for circuit breakers and `axios-retry` for retry mechanisms.

## Dependencies

```bash
# Core error handling
npm install opossum axios axios-retry

# AWS services for messaging
npm install aws-sdk

# Redis for caching (not messaging)
npm install ioredis

# Development dependencies
npm install --save-dev @types/node @types/aws-sdk
```

## Error Categories

### 1. Network/Communication Errors
- Connection timeouts (ECONNRESET, ETIMEDOUT)
- Connection refused (ECONNREFUSED)
- DNS resolution failures (ENOTFOUND)
- SSL/TLS handshake failures

### 2. Service Errors
- HTTP 5xx server errors
- Service unavailable (503)
- Gateway timeout (504)
- Rate limiting (429)

### 3. Application Errors
- Business logic validation failures
- Data consistency issues
- Authentication/authorization failures

### 4. Infrastructure Errors
- Database connection failures
- Message queue unavailability
- Redis/cache failures

## Circuit Breaker with Opossum

### Circuit Breaker Configuration

```typescript
import CircuitBreaker from 'opossum';

interface CircuitBreakerOptions {
  timeout: number;              // Request timeout (ms)
  errorThresholdPercentage: number; // Percentage of failures before opening
  resetTimeout: number;         // Time before attempting recovery (ms)
  rollingCountTimeout: number;  // Time window for failure counting (ms)
  rollingCountBuckets: number;  // Number of buckets in time window
  volumeThreshold: number;      // Minimum requests before considering failure rate
  name: string;                 // Circuit breaker name for monitoring
}

const createCircuitBreakerOptions = (serviceName: string): CircuitBreakerOptions => ({
  timeout: 5000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000,
  rollingCountTimeout: 60000,
  rollingCountBuckets: 10,
  volumeThreshold: 10,
  name: serviceName
});
```

### Circuit Breaker Factory

```typescript
class CircuitBreakerFactory {
  private static breakers = new Map<string, CircuitBreaker>();

  static getCircuitBreaker<T>(
    serviceName: string,
    action: (...args: any[]) => Promise<T>,
    options?: Partial<CircuitBreakerOptions>
  ): CircuitBreaker {
    if (this.breakers.has(serviceName)) {
      return this.breakers.get(serviceName)!;
    }

    const defaultOptions = createCircuitBreakerOptions(serviceName);
    const finalOptions = { ...defaultOptions, ...options };

    const breaker = new CircuitBreaker(action, finalOptions);

    // Event listeners for monitoring
    breaker.on('open', () => {
      logger.warn('Circuit breaker opened', { service: serviceName });
    });

    breaker.on('halfOpen', () => {
      logger.info('Circuit breaker half-open', { service: serviceName });
    });

    breaker.on('close', () => {
      logger.info('Circuit breaker closed', { service: serviceName });
    });

    breaker.on('fallback', (data) => {
      logger.warn('Circuit breaker fallback executed', { 
        service: serviceName, 
        data 
      });
    });

    this.breakers.set(serviceName, breaker);
    return breaker;
  }

  static getMetrics(): Record<string, any> {
    const metrics: Record<string, any> = {};
    
    for (const [name, breaker] of this.breakers) {
      metrics[name] = {
        state: breaker.opened ? 'OPEN' : breaker.halfOpen ? 'HALF_OPEN' : 'CLOSED',
        stats: breaker.stats
      };
    }
    
    return metrics;
  }
}
```

## Retry Mechanisms with Axios-Retry

### Axios Instance with Retry Configuration

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';
import axiosRetry from 'axios-retry';

interface RetryConfig {
  retries: number;
  retryDelay: (retryCount: number) => number;
  retryCondition: (error: AxiosError) => boolean;
  shouldResetTimeout: boolean;
}

class HttpClientFactory {
  static createClient(serviceName: string, baseURL: string): AxiosInstance {
    const client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': `sales-api-client/${serviceName}`
      }
    });

    // Configure retry logic
    axiosRetry(client, {
      retries: 3,
      retryDelay: axiosRetry.exponentialDelay,
      retryCondition: (error: AxiosError) => {
        // Retry on network errors and 5xx responses
        return axiosRetry.isNetworkOrIdempotentRequestError(error) ||
               (error.response?.status ?? 0) >= 500;
      },
      shouldResetTimeout: true,
      onRetry: (retryCount, error) => {
        logger.warn('HTTP request retry', {
          service: serviceName,
          retryCount,
          error: error.message,
          url: error.config?.url
        });
      }
    });

    // Request interceptor for logging
    client.interceptors.request.use(
      (config) => {
        logger.debug('HTTP request', {
          service: serviceName,
          method: config.method?.toUpperCase(),
          url: config.url
        });
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for logging
    client.interceptors.response.use(
      (response) => {
        logger.debug('HTTP response', {
          service: serviceName,
          status: response.status,
          url: response.config.url
        });
        return response;
      },
      (error) => {
        logger.error('HTTP error', {
          service: serviceName,
          status: error.response?.status,
          message: error.message,
          url: error.config?.url
        });
        return Promise.reject(error);
      }
    );

    return client;
  }
}
```

## Service-Specific Error Handling

### 1. Product Service Client (Sales API)

```typescript
import CircuitBreaker from 'opossum';

interface ProductAvailability {
  productId: string;
  available: boolean;
  quantity: number;
  requiresManualReview?: boolean;
  fallbackUsed?: boolean;
}

class ProductServiceClient {
  private httpClient: AxiosInstance;
  private circuitBreaker: CircuitBreaker;

  constructor() {
    // Create HTTP client with retry logic
    this.httpClient = HttpClientFactory.createClient(
      'product-service', 
      process.env.PRODUCT_SERVICE_URL || 'http://localhost:3003'
    );

    // Configure circuit breaker
    this.circuitBreaker = CircuitBreakerFactory.getCircuitBreaker(
      'product-service',
      this.makeAvailabilityRequest.bind(this),
      {
        timeout: 5000,
        errorThresholdPercentage: 50,
        resetTimeout: 30000,
        volumeThreshold: 10
      }
    );

    // Set up fallback
    this.circuitBreaker.fallback((productIds: string[]) => {
      logger.warn('Using fallback for product availability check', { productIds });
      return productIds.map(productId => ({
        productId,
        available: true,
        quantity: 1,
        requiresManualReview: true,
        fallbackUsed: true
      }));
    });
  }

  private async makeAvailabilityRequest(productIds: string[]): Promise<ProductAvailability[]> {
    const response = await this.httpClient.post('/check-availability', { productIds });
    return response.data;
  }

  async checkAvailability(productIds: string[]): Promise<ProductAvailability[]> {
    try {
      return await this.circuitBreaker.fire(productIds);
    } catch (error) {
      logger.error('Product availability check failed completely', {
        productIds,
        error: error.message
      });
      throw error;
    }
  }
}
```

### 2. Delivery Service Client (Sales API)

```typescript
interface DeliveryInitiationData {
  orderId: string;
  customerId: string;
  products: Array<{
    productId: string;
    quantity: number;
  }>;
  shippingAddress: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
}

interface DeliveryResponse {
  deliveryId: string;
  trackingNumber: string;
  estimatedDeliveryDate: string;
  carrier: string;
}

class DeliveryServiceClient {
  private httpClient: AxiosInstance;
  private circuitBreaker: CircuitBreaker;

  constructor() {
    // Create HTTP client with retry logic (less aggressive for order creation)
    this.httpClient = HttpClientFactory.createClient(
      'delivery-service',
      process.env.DELIVERY_SERVICE_URL || 'http://localhost:3002'
    );

    // Override retry config for delivery service
    axiosRetry(this.httpClient, {
      retries: 2, // Less aggressive for order creation
      retryDelay: (retryCount) => retryCount * 2000, // Linear backoff
      retryCondition: (error: AxiosError) => {
        // Only retry on specific network errors, not all 5xx
        return axiosRetry.isNetworkError(error) || 
               error.response?.status === 503 || 
               error.response?.status === 504;
      },
      shouldResetTimeout: true
    });

    // Configure circuit breaker (more sensitive for order operations)
    this.circuitBreaker = CircuitBreakerFactory.getCircuitBreaker(
      'delivery-service',
      this.makeDeliveryRequest.bind(this),
      {
        timeout: 10000,
        errorThresholdPercentage: 40, // More sensitive
        resetTimeout: 60000,
        volumeThreshold: 5
      }
    );
  }

  private async makeDeliveryRequest(orderData: DeliveryInitiationData): Promise<DeliveryResponse> {
    const response = await this.httpClient.post('/deliveries', orderData);
    return response.data;
  }

  async initiateDelivery(orderData: DeliveryInitiationData): Promise<DeliveryResponse> {
    return this.circuitBreaker.fire(orderData);
  }
}
```

### 3. Database Error Handling with Prisma

```typescript
import { PrismaClient } from '@prisma/client';

class DatabaseService {
  private prisma: PrismaClient;
  private circuitBreaker: CircuitBreaker;

  constructor() {
    this.prisma = new PrismaClient({
      log: ['query', 'error', 'warn'],
      errorFormat: 'pretty'
    });

    // Circuit breaker for database operations
    this.circuitBreaker = CircuitBreakerFactory.getCircuitBreaker(
      'database',
      this.executeQuery.bind(this),
      {
        timeout: 3000,
        errorThresholdPercentage: 60,
        resetTimeout: 20000,
        volumeThreshold: 10
      }
    );
  }

  private async executeQuery<T>(operation: () => Promise<T>): Promise<T> {
    try {
      return await operation();
    } catch (error) {
      // Check if it's a retryable database error
      if (this.isRetryableDbError(error)) {
        throw error; // Let circuit breaker handle retry logic
      }
      // Non-retryable errors (e.g., constraint violations)
      throw new Error(`Database error: ${error.message}`);
    }
  }

  private isRetryableDbError(error: any): boolean {
    const retryableCodes = [
      'P2024', // Timed out fetching a new connection from the connection pool
      'P2034', // Transaction failed due to a write conflict or a deadlock
      'P1001', // Can't reach database server
      'P1002', // The database server timed out
      'P1008', // Operations timed out
      'P1017'  // Server has closed the connection
    ];

    return retryableCodes.includes(error.code) || 
           error.message.includes('ECONNRESET') ||
           error.message.includes('ETIMEDOUT');
  }

  async executeWithCircuitBreaker<T>(operation: () => Promise<T>): Promise<T> {
    return this.circuitBreaker.fire(operation);
  }

  // Example usage methods
  async createOrder(orderData: any) {
    return this.executeWithCircuitBreaker(() => 
      this.prisma.order.create({ data: orderData })
    );
  }

  async updateOrderStatus(orderId: string, status: string) {
    return this.executeWithCircuitBreaker(() =>
      this.prisma.order.update({
        where: { id: orderId },
        data: { status, updatedAt: new Date() }
      })
    );
  }
}
```

## Event Publishing Error Handling with AWS SQS/SNS

```typescript
import AWS from 'aws-sdk';

interface EventMessage {
  eventType: string;
  eventData: any;
  timestamp: Date;
  messageId: string;
  source: string;
}

interface EventPublishingConfig {
  region: string;
  topicArn: string;
  deadLetterQueueUrl: string;
}

class EventPublisher {
  private sns: AWS.SNS;
  private sqs: AWS.SQS;
  private circuitBreaker: CircuitBreaker;
  private config: EventPublishingConfig;

  constructor(config: EventPublishingConfig) {
    this.config = config;
    
    AWS.config.update({ region: config.region });
    this.sns = new AWS.SNS();
    this.sqs = new AWS.SQS();

    // Circuit breaker for event publishing
    this.circuitBreaker = CircuitBreakerFactory.getCircuitBreaker(
      'event-publisher',
      this.sendToSNS.bind(this),
      {
        timeout: 5000,
        errorThresholdPercentage: 70,
        resetTimeout: 30000,
        volumeThreshold: 10
      }
    );

    // Fallback to dead letter queue
    this.circuitBreaker.fallback(async (eventMessage: EventMessage) => {
      await this.sendToDeadLetterQueue(eventMessage, 'Circuit breaker fallback');
      logger.warn('Event sent to DLQ via circuit breaker fallback', {
        eventType: eventMessage.eventType,
        messageId: eventMessage.messageId
      });
    });
  }

  private async sendToSNS(eventMessage: EventMessage): Promise<void> {
    const params: AWS.SNS.PublishInput = {
      TopicArn: this.config.topicArn,
      Message: JSON.stringify(eventMessage),
      MessageAttributes: {
        'event-type': {
          DataType: 'String',
          StringValue: eventMessage.eventType
        },
        'source': {
          DataType: 'String',
          StringValue: eventMessage.source
        },
        'timestamp': {
          DataType: 'String',
          StringValue: eventMessage.timestamp.toISOString()
        }
      },
      // MANDATORY FIFO Configuration
      MessageGroupId: this.getMessageGroupId(eventMessage), // Critical for FIFO ordering
      MessageDeduplicationId: eventMessage.messageId
    };

    const result = await this.sns.publish(params).promise();
    logger.debug('Event published to SNS FIFO', {
      messageId: result.MessageId,
      eventType: eventMessage.eventType,
      messageGroupId: params.MessageGroupId
    });
  }

  private getMessageGroupId(eventMessage: EventMessage): string {
    // Group messages by order for strict ordering within each order
    if (eventMessage.eventData.orderId) {
      return `order-${eventMessage.eventData.orderId}`;
    }
    
    // Group by customer for customer-level ordering
    if (eventMessage.eventData.customerId) {
      return `customer-${eventMessage.eventData.customerId}`;
    }
    
    // Fallback to event type (less strict ordering)
    return eventMessage.eventType;
  }

  private async sendToDeadLetterQueue(eventMessage: EventMessage, errorReason: string): Promise<void> {
    const dlqMessage = {
      ...eventMessage,
      errorReason,
      failedAt: new Date(),
      originalMessageId: eventMessage.messageId
    };

    const params: AWS.SQS.SendMessageRequest = {
      QueueUrl: this.config.deadLetterQueueUrl,
      MessageBody: JSON.stringify(dlqMessage),
      MessageAttributes: {
        'error-reason': {
          DataType: 'String',
          StringValue: errorReason
        },
        'original-event-type': {
          DataType: 'String',
          StringValue: eventMessage.eventType
        }
      }
    };

    await this.sqs.sendMessage(params).promise();
    logger.warn('Message sent to dead letter queue', {
      originalMessageId: eventMessage.messageId,
      errorReason
    });
  }

  async publishEvent(eventType: string, eventData: any, source: string = 'sales-api'): Promise<void> {
    const eventMessage: EventMessage = {
      eventType,
      eventData,
      timestamp: new Date(),
      messageId: `${eventType}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      source
    };

    try {
      await this.circuitBreaker.fire(eventMessage);
      logger.info('Event published successfully', {
        eventType,
        messageId: eventMessage.messageId,
        source
      });
    } catch (error) {
      logger.error('Event publishing failed completely', {
        eventType,
        messageId: eventMessage.messageId,
        error: error.message
      });
      throw error;
    }
  }

  // Utility method to process DLQ messages
  async processDLQMessages(maxMessages: number = 10): Promise<void> {
    const params: AWS.SQS.ReceiveMessageRequest = {
      QueueUrl: this.config.deadLetterQueueUrl,
      MaxNumberOfMessages: maxMessages,
      WaitTimeSeconds: 10,
      MessageAttributeNames: ['All']
    };

    const result = await this.sqs.receiveMessage(params).promise();
    
    if (result.Messages) {
      for (const message of result.Messages) {
        try {
          const dlqMessage = JSON.parse(message.Body!);
          logger.info('Processing DLQ message', {
            originalMessageId: dlqMessage.originalMessageId,
            eventType: dlqMessage.eventType,
            errorReason: dlqMessage.errorReason
          });

          // Attempt to republish or handle manually
          // Implementation depends on business requirements

          // Delete message from DLQ after processing
          await this.sqs.deleteMessage({
            QueueUrl: this.config.deadLetterQueueUrl,
            ReceiptHandle: message.ReceiptHandle!
          }).promise();

        } catch (error) {
          logger.error('Failed to process DLQ message', {
            messageId: message.MessageId,
            error: error.message
          });
        }
      }
    }
  }
}
```

## Configuration Management

### Environment-Based Configurations

```typescript
interface ServiceConfig {
  circuitBreaker: Partial<CircuitBreakerOptions>;
  axiosRetry: {
    retries: number;
    retryDelay: 'exponential' | 'linear' | 'fixed';
    baseDelay?: number;
  };
  timeout: number;
}

class ConfigurationManager {
  private static configs: Record<string, ServiceConfig> = {
    'product-service': {
      circuitBreaker: {
        timeout: 5000,
        errorThresholdPercentage: process.env.NODE_ENV === 'production' ? 50 : 40,
        resetTimeout: 30000,
        volumeThreshold: 10
      },
      axiosRetry: {
        retries: 3,
        retryDelay: 'exponential'
      },
      timeout: 5000
    },
    'delivery-service': {
      circuitBreaker: {
        timeout: 10000,
        errorThresholdPercentage: 40, // More sensitive for order operations
        resetTimeout: 60000,
        volumeThreshold: 5
      },
      axiosRetry: {
        retries: 2, // Less aggressive for order creation
        retryDelay: 'linear',
        baseDelay: 2000
      },
      timeout: 10000
    },
    'database': {
      circuitBreaker: {
        timeout: 3000,
        errorThresholdPercentage: 60,
        resetTimeout: 20000,
        volumeThreshold: 10
      },
      axiosRetry: {
        retries: 3,
        retryDelay: 'exponential',
        baseDelay: 500
      },
      timeout: 3000
    },
    'event-broker': {
      circuitBreaker: {
        timeout: 2000,
        errorThresholdPercentage: 70,
        resetTimeout: 30000,
        volumeThreshold: 20
      },
      axiosRetry: {
        retries: 5,
        retryDelay: 'exponential'
      },
      timeout: 2000
    }
  };

  static getConfig(serviceName: string): ServiceConfig {
    return this.configs[serviceName] || this.getDefaultConfig();
  }

  private static getDefaultConfig(): ServiceConfig {
    return {
      circuitBreaker: {
        timeout: 5000,
        errorThresholdPercentage: 50,
        resetTimeout: 30000,
        volumeThreshold: 10
      },
      axiosRetry: {
        retries: 3,
        retryDelay: 'exponential'
      },
      timeout: 5000
    };
  }

      static createRetryDelayFunction(config: ServiceConfig['axiosRetry']) {
      switch (config.retryDelay) {
        case 'exponential':
          return axiosRetry.exponentialDelay;
        case 'linear':
          return (retryCount: number) => (config.baseDelay || 1000) * retryCount;
        case 'fixed':
          return () => config.baseDelay || 1000;
        default:
          return axiosRetry.exponentialDelay;
      }
    }
  }
  ```

  ## FIFO Queue Requirements & Configuration

### Why FIFO is Mandatory

For e-commerce order processing, **message ordering is critical**:

```typescript
// WRONG ORDER = DATA CORRUPTION
1. ORDER_CREATED (orderId: "123", status: "PENDING_SHIPMENT")
2. ORDER_SHIPPED (orderId: "123", status: "SHIPPED")  
3. ORDER_CANCELLED (orderId: "123", status: "CANCELLED") // ❌ Out of order!

// CORRECT ORDER = DATA CONSISTENCY  
1. ORDER_CREATED (orderId: "123", status: "PENDING_SHIPMENT")
2. ORDER_CANCELLED (orderId: "123", status: "CANCELLED")
3. ORDER_SHIPPED (orderId: "123", status: "SHIPPED") // ✅ Rejected - invalid transition
```

### AWS SQS FIFO Capabilities

**✅ What SQS FIFO Provides:**
- **Exactly-once processing** - No duplicate messages
- **Strict message ordering** - Within message groups
- **Content-based deduplication** - Automatic duplicate detection
- **Message group partitioning** - Parallel processing with ordering

**⚠️ SQS FIFO Limitations:**
- **Throughput limit**: 300 TPS (transactions per second)
- **Batching limit**: 3,000 TPS (with 10 messages per batch)
- **Regional only**: No cross-region replication
- **Higher cost**: ~2x more expensive than standard SQS

### FIFO Configuration Strategy

```typescript
// Message Group ID Strategy (Critical for Performance)
private getMessageGroupId(eventMessage: EventMessage): string {
  // Option 1: Per-Order Ordering (Strictest)
  if (eventMessage.eventData.orderId) {
    return `order-${eventMessage.eventData.orderId}`;
  }
  
  // Option 2: Per-Customer Ordering (Balanced)
  if (eventMessage.eventData.customerId) {
    return `customer-${eventMessage.eventData.customerId}`;
  }
  
  // Option 3: Per-EventType (Loosest)
  return eventMessage.eventType;
}
```

### Performance Considerations

**Throughput Analysis:**
```typescript
// Scenario 1: Per-Order Grouping
// - Perfect ordering per order
// - Max throughput: 300 orders/second
// - Good for: Medium volume e-commerce

// Scenario 2: Per-Customer Grouping  
// - Ordering within customer's orders
// - Max throughput: 300 customers/second processing simultaneously
// - Good for: High volume with many customers

// Scenario 3: Per-EventType Grouping
// - Ordering within event types
// - Max throughput: 300 events/second per type
// - Good for: Very high volume, relaxed ordering
```

### Scaling Beyond FIFO Limits

**If 300 TPS is insufficient:**

```typescript
// Option 1: Partition by Region/Shard
const shardId = hashFunction(orderId) % numberOfShards;
const messageGroupId = `shard-${shardId}-order-${orderId}`;

// Option 2: Hybrid Approach (Critical vs Non-Critical)
if (isCriticalEvent(eventType)) {
  await publishToFIFO(event); // Guaranteed ordering
} else {
  await publishToStandard(event); // Higher throughput
}

// Option 3: Move to Apache Kafka
// - Supports millions of messages/second
// - Partition-level ordering
// - More complex infrastructure
```

## AWS Infrastructure Configuration

  ### Environment Variables

  ```bash
  # AWS Configuration
  AWS_REGION=us-east-1
  AWS_ACCESS_KEY_ID=your-access-key
  AWS_SECRET_ACCESS_KEY=your-secret-key

  # SNS Topic for Order Events
  ORDER_EVENTS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:order-events

  # SQS Dead Letter Queue
  DLQ_URL=https://sqs.us-east-1.amazonaws.com/123456789012/order-events-dlq

  # Redis Cache Configuration
  REDIS_HOST=localhost
  REDIS_PORT=6379
  REDIS_KEY_PREFIX=ecommerce:
  ```

  ### AWS Resource Setup (Terraform Example)

  ```hcl
  # SNS FIFO Topic for Order Events (MANDATORY for ordering)
  resource "aws_sns_topic" "order_events" {
    name                        = "order-events.fifo"  # Must end with .fifo
    fifo_topic                  = true                 # MANDATORY: Enable FIFO
    content_based_deduplication = true                 # MANDATORY: Prevent duplicates
    
    tags = {
      Environment = "production"
      Service     = "order-processing"
      MessageOrdering = "required"
    }
  }

  # SQS Queue for Delivery Service
  resource "aws_sqs_queue" "delivery_processing" {
    name                       = "delivery-processing.fifo"
    fifo_queue                 = true
    content_based_deduplication = true
    visibility_timeout_seconds = 300
    message_retention_seconds  = 1209600 # 14 days
    
    redrive_policy = jsonencode({
      deadLetterTargetArn = aws_sqs_queue.delivery_dlq.arn
      maxReceiveCount     = 3
    })
  }

  # Dead Letter Queue
  resource "aws_sqs_queue" "delivery_dlq" {
    name                       = "delivery-processing-dlq.fifo"
    fifo_queue                 = true
    content_based_deduplication = true
    message_retention_seconds  = 1209600 # 14 days
  }

  # SNS Subscription
  resource "aws_sns_topic_subscription" "delivery_subscription" {
    topic_arn = aws_sns_topic.order_events.arn
    protocol  = "sqs"
    endpoint  = aws_sqs_queue.delivery_processing.arn
    
    filter_policy = jsonencode({
      "event-type" = ["ORDER_CREATED", "ORDER_UPDATED"]
    })
  }

  # IAM Policy for Event Publishing
  resource "aws_iam_policy" "event_publisher_policy" {
    name = "event-publisher-policy"
    
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "sns:Publish"
          ]
          Resource = aws_sns_topic.order_events.arn
        },
        {
          Effect = "Allow"
          Action = [
            "sqs:SendMessage",
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage"
          ]
          Resource = [
            aws_sqs_queue.delivery_dlq.arn
          ]
        }
      ]
    })
  }
  ```

  ### Service Integration Example

  ```typescript
  // Configuration setup
  const eventPublisher = new EventPublisher({
    region: process.env.AWS_REGION || 'us-east-1',
    topicArn: process.env.ORDER_EVENTS_TOPIC_ARN!,
    deadLetterQueueUrl: process.env.DLQ_URL!
  });

  const cacheService = new CacheService({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    retryDelayOnFailover: 100,
    maxRetriesPerRequest: 3,
    keyPrefix: process.env.REDIS_KEY_PREFIX || 'ecommerce:'
  });

  // Usage in order creation
  async function createOrder(orderData: any) {
    try {
      // Create order in database
      const order = await database.createOrder(orderData);
      
      // Cache order for quick access
      await cacheService.cacheProduct(order.id, order, 300);
      
      // Publish event for other services
      await eventPublisher.publishEvent('ORDER_CREATED', {
        orderId: order.id,
        customerId: order.customerId,
        products: order.products,
        timestamp: order.createdAt
      }, 'sales-api');
      
      return order;
    } catch (error) {
      logger.error('Order creation failed', { error: error.message });
      throw error;
    }
  }
  ```

## Monitoring and Metrics

### Health Check Integration

```typescript
interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  circuitBreakers: Array<{
    service: string;
    state: 'CLOSED' | 'OPEN' | 'HALF_OPEN';
    stats: any;
  }>;
  timestamp: Date;
}

class HealthCheckService {
  getHealthStatus(): HealthStatus {
    const circuitBreakerMetrics = CircuitBreakerFactory.getMetrics();
    const circuitBreakerStatuses = Object.entries(circuitBreakerMetrics).map(
      ([name, metrics]) => ({
        service: name,
        state: metrics.state as 'CLOSED' | 'OPEN' | 'HALF_OPEN',
        stats: metrics.stats
      })
    );

    const hasOpenCircuits = circuitBreakerStatuses.some(
      status => status.state === 'OPEN'
    );

    const hasHalfOpenCircuits = circuitBreakerStatuses.some(
      status => status.state === 'HALF_OPEN'
    );

    let overallStatus: 'healthy' | 'degraded' | 'unhealthy';
    if (hasOpenCircuits) {
      overallStatus = 'unhealthy';
    } else if (hasHalfOpenCircuits) {
      overallStatus = 'degraded';
    } else {
      overallStatus = 'healthy';
    }

    return {
      status: overallStatus,
      circuitBreakers: circuitBreakerStatuses,
      timestamp: new Date()
    };
  }

  // Health check endpoint handler
  async handleHealthCheck(req: express.Request, res: express.Response): Promise<void> {
    const healthStatus = this.getHealthStatus();
    
    const statusCode = healthStatus.status === 'healthy' ? 200 :
                      healthStatus.status === 'degraded' ? 200 : 503;

    res.status(statusCode).json(healthStatus);
  }
}
```

## Redis for Caching (Proper Use Case)

```typescript
import Redis from 'ioredis';

interface CacheConfig {
  host: string;
  port: number;
  retryDelayOnFailover: number;
  maxRetriesPerRequest: number;
  keyPrefix: string;
}

class CacheService {
  private redis: Redis;
  private circuitBreaker: CircuitBreaker;

  constructor(config: CacheConfig) {
    this.redis = new Redis({
      host: config.host,
      port: config.port,
      retryDelayOnFailover: config.retryDelayOnFailover,
      maxRetriesPerRequest: config.maxRetriesPerRequest,
      keyPrefix: config.keyPrefix,
      lazyConnect: true
    });

    // Circuit breaker for cache operations
    this.circuitBreaker = CircuitBreakerFactory.getCircuitBreaker(
      'redis-cache',
      this.executeRedisOperation.bind(this),
      {
        timeout: 1000,
        errorThresholdPercentage: 80, // More tolerant for cache
        resetTimeout: 15000,
        volumeThreshold: 5
      }
    );

    // Fallback for cache misses (when Redis is down)
    this.circuitBreaker.fallback(() => null);
  }

  private async executeRedisOperation<T>(operation: () => Promise<T>): Promise<T> {
    return operation();
  }

  // Product caching
  async cacheProduct(productId: string, productData: any, ttl: number = 300): Promise<void> {
    try {
      await this.circuitBreaker.fire(() =>
        this.redis.setex(`product:${productId}`, ttl, JSON.stringify(productData))
      );
    } catch (error) {
      logger.warn('Failed to cache product', { productId, error: error.message });
      // Gracefully continue without caching
    }
  }

  async getCachedProduct(productId: string): Promise<any | null> {
    try {
      const result = await this.circuitBreaker.fire(() =>
        this.redis.get(`product:${productId}`)
      );
      return result ? JSON.parse(result) : null;
    } catch (error) {
      logger.warn('Cache miss due to error', { productId, error: error.message });
      return null; // Cache miss, fetch from database
    }
  }

  // Session management
  async setSession(sessionId: string, sessionData: any, ttl: number = 1800): Promise<void> {
    try {
      await this.circuitBreaker.fire(() =>
        this.redis.setex(`session:${sessionId}`, ttl, JSON.stringify(sessionData))
      );
    } catch (error) {
      logger.warn('Failed to store session', { sessionId, error: error.message });
      // For sessions, this might be more critical - could throw or use fallback storage
    }
  }

  async getSession(sessionId: string): Promise<any | null> {
    try {
      const result = await this.circuitBreaker.fire(() =>
        this.redis.get(`session:${sessionId}`)
      );
      return result ? JSON.parse(result) : null;
    } catch (error) {
      logger.warn('Session lookup failed', { sessionId, error: error.message });
      return null;
    }
  }

  // Rate limiting
  async checkRateLimit(clientId: string, limit: number, windowSeconds: number): Promise<boolean> {
    try {
      const key = `rate_limit:${clientId}`;
      const current = await this.circuitBreaker.fire(() => this.redis.incr(key));
      
      if (current === 1) {
        await this.redis.expire(key, windowSeconds);
      }
      
      return current <= limit;
    } catch (error) {
      logger.warn('Rate limiting failed, allowing request', { clientId, error: error.message });
      return true; // Fail open for rate limiting
    }
  }

  // Health check
  async isHealthy(): Promise<boolean> {
    try {
      await this.redis.ping();
      return true;
    } catch (error) {
      return false;
    }
  }
}
```

## Integration with Express.js

### Error Handling Middleware

```typescript
import express from 'express';
import { AxiosError } from 'axios';

class ErrorHandlingMiddleware {
  static handle() {
    return (error: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
      // Circuit breaker errors (opossum)
      if (error.message.includes('Circuit breaker is open')) {
        return res.status(503).json({
          error: 'Service temporarily unavailable',
          message: 'Please try again later',
          retryAfter: 30
        });
      }

      // Axios timeout errors
      if (error.message.includes('timeout') || error.name === 'ETIMEDOUT') {
        return res.status(504).json({
          error: 'Request timeout',
          message: 'The request took too long to process'
        });
      }

      // Axios network errors
      if (error instanceof AxiosError) {
        if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
          return res.status(502).json({
            error: 'Service unavailable',
            message: 'Unable to connect to required service'
          });
        }

        if (error.response?.status && error.response.status >= 500) {
          return res.status(502).json({
            error: 'Upstream service error',
            message: 'Service returned an error response'
          });
        }

        if (error.response?.status === 429) {
          return res.status(429).json({
            error: 'Rate limit exceeded',
            message: 'Too many requests',
            retryAfter: error.response.headers['retry-after'] || 60
          });
        }
      }

      // Database/Prisma errors
      if (error.message.includes('Prisma') || error.name.includes('Prisma')) {
        logger.error('Database error', {
          error: error.message,
          path: req.path,
          method: req.method
        });

        return res.status(500).json({
          error: 'Database error',
          message: 'Unable to process request due to database issue'
        });
      }

      // Default error handler
      logger.error('Unhandled error', {
        error: error.message,
        stack: error.stack,
        path: req.path,
        method: req.method,
        requestId: req.headers['x-request-id']
      });

      res.status(500).json({
        error: 'Internal server error',
        message: 'An unexpected error occurred'
      });
    };
  }

  // Request timeout middleware
  static timeout(timeoutMs: number = 30000) {
    return (req: express.Request, res: express.Response, next: express.NextFunction) => {
      const timeout = setTimeout(() => {
        if (!res.headersSent) {
          res.status(408).json({
            error: 'Request timeout',
            message: `Request took longer than ${timeoutMs}ms`
          });
        }
      }, timeoutMs);

      res.on('finish', () => {
        clearTimeout(timeout);
      });

      next();
    };
  }
}
```

## Testing Strategy

### Unit Tests

```typescript
import CircuitBreaker from 'opossum';
import axios from 'axios';
import axiosRetry from 'axios-retry';

describe('Circuit Breaker with Opossum', () => {
  test('should open circuit after threshold failures', async () => {
    const failingOperation = jest.fn().mockRejectedValue(new Error('Service failed'));
    
    const cb = new CircuitBreaker(failingOperation, {
      timeout: 1000,
      errorThresholdPercentage: 50,
      resetTimeout: 5000,
      volumeThreshold: 2
    });

    // Simulate failures to reach threshold
    for (let i = 0; i < 3; i++) {
      try {
        await cb.fire();
      } catch {}
    }

    expect(cb.opened).toBe(true);
    expect(failingOperation).toHaveBeenCalledTimes(3);
  });

  test('should use fallback when circuit is open', async () => {
    const failingOperation = jest.fn().mockRejectedValue(new Error('Service failed'));
    const fallbackValue = 'fallback-response';
    
    const cb = new CircuitBreaker(failingOperation, {
      timeout: 1000,
      errorThresholdPercentage: 50,
      resetTimeout: 5000,
      volumeThreshold: 1
    });

    cb.fallback(() => fallbackValue);

    // Cause circuit to open
    try { await cb.fire(); } catch {}
    try { await cb.fire(); } catch {}

    // Should now use fallback
    const result = await cb.fire();
    expect(result).toBe(fallbackValue);
  });
});

describe('Axios Retry Integration', () => {
  test('should retry on network errors', async () => {
    const mockAdapter = {
      onGet: jest.fn()
    };

    const client = axios.create();
    axiosRetry(client, {
      retries: 2,
      retryCondition: (error) => axiosRetry.isNetworkError(error)
    });

    // Mock network error followed by success
    const mockRequest = jest.fn()
      .mockRejectedValueOnce({ code: 'ECONNRESET' })
      .mockRejectedValueOnce({ code: 'ECONNRESET' })
      .mockResolvedValueOnce({ data: 'success' });

    client.defaults.adapter = mockRequest;

    const response = await client.get('/test');
    expect(response.data).toBe('success');
    expect(mockRequest).toHaveBeenCalledTimes(3);
  });
});

describe('ProductServiceClient', () => {
  test('should use fallback when service fails', async () => {
    const client = new ProductServiceClient();
    
    // Mock HTTP client to fail
    jest.spyOn(client['httpClient'], 'post').mockRejectedValue(new Error('Service down'));

    const result = await client.checkAvailability(['product1', 'product2']);
    
    expect(result).toEqual([
      { productId: 'product1', available: true, quantity: 1, requiresManualReview: true, fallbackUsed: true },
      { productId: 'product2', available: true, quantity: 1, requiresManualReview: true, fallbackUsed: true }
    ]);
  });
});

describe('DatabaseService', () => {
  test('should handle retryable database errors', async () => {
    const service = new DatabaseService();
    
    const mockOperation = jest.fn()
      .mockRejectedValueOnce({ code: 'P1001' }) // Connection error
      .mockResolvedValueOnce('success');

    const result = await service.executeWithCircuitBreaker(mockOperation);
    
    expect(result).toBe('success');
    expect(mockOperation).toHaveBeenCalledTimes(2);
  });
});
```

### Integration Tests

```typescript
describe('End-to-End Error Handling', () => {
  test('should handle complete service failure gracefully', async () => {
    // Start with all services down
    const app = createTestApp();
    
    const response = await request(app)
      .post('/orders')
      .send({
        customerId: 'customer-1',
        products: [{ productId: 'product-1', quantity: 1 }]
      });

    expect(response.status).toBe(503);
    expect(response.body.error).toBe('Service temporarily unavailable');
  });

  test('should recover when services come back online', async () => {
    // Test circuit breaker recovery
    const app = createTestApp();
    
    // Simulate service recovery after failures
    // ... test implementation
  });
});
```

## Package.json Dependencies

Add these dependencies to your project:

```json
{
  "dependencies": {
    "opossum": "^6.3.0",
    "axios": "^1.6.0",
    "axios-retry": "^3.8.0",
    "aws-sdk": "^2.1691.0",
    "ioredis": "^5.3.0",
    "express": "^4.18.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/aws-sdk": "^2.7.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
```

This comprehensive error handling design leverages proven npm libraries and AWS managed services:
- **`opossum`** and **`axios-retry`** for robust resilience patterns
- **AWS SQS/SNS** for reliable event messaging with built-in DLQ support
- **Redis** for proper caching use cases (product data, sessions, rate limiting)

This architecture ensures graceful degradation and system stability under various failure conditions while using each technology for its intended purpose. 