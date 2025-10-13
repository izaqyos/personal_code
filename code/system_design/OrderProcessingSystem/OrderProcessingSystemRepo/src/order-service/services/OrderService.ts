import { v4 as uuidv4 } from 'uuid';
import { Database, redis, sqs, logger } from '../../shared';
import { 
  CreateOrderRequest, 
  Order, 
  OrderItem, 
  OrderCreatedEvent 
} from '../../shared';

export class OrderService {
  // Simple order creation for PoC
  // Production would have:
  // - Product availability checks, inventory management,
  // - Payment processing, order validation,
  // - Distributed transactions, saga patterns

  async createOrder(request: CreateOrderRequest): Promise<Order> {
    const orderId = uuidv4();
    const now = new Date();
    
    // Generate idempotency fingerprint
    const fingerprint = redis.generateFingerprint(
      request.customer_id,
      request.items
    );

    // Check for duplicate request
    const existingResult = await redis.checkIdempotency(fingerprint);
    if (existingResult) {
      logger.info('Returning cached order result', { fingerprint });
      return JSON.parse(existingResult);
    }

    // Calculate total amount
    const totalAmount = request.items.reduce(
      (sum, item) => sum + (item.quantity * item.unit_price),
      0
    );

    // Use database transaction for ACID properties
    const order = await Database.transaction(async (client) => {
      // Insert order
      const orderResult = await client.query(
        `INSERT INTO orders (id, customer_id, status, total_amount, created_at, updated_at)
         VALUES ($1, $2, $3, $4, $5, $6)
         RETURNING *`,
        [orderId, request.customer_id, 'PENDING_SHIPMENT', totalAmount, now, now]
      );

      // Insert order items
      for (const item of request.items) {
        await client.query(
          `INSERT INTO order_items (order_id, product_id, quantity, unit_price)
           VALUES ($1, $2, $3, $4)`,
          [orderId, item.product_id, item.quantity, item.unit_price]
        );
      }

      return orderResult.rows[0];
    });

    // Publish event to SQS for delivery service
    // Production would handle SQS failures with retry logic
    try {
      const event: OrderCreatedEvent = {
        eventType: 'ORDER_CREATED',
        orderId: order.id,
        customerId: order.customer_id,
        items: request.items,
        totalAmount: order.total_amount,
        timestamp: now,
      };

      // HYBRID FIFO: Time-partitioned ordering optimized for fairness
      // Orders within 30-second windows are processed in strict FIFO order
      // Fewer partitions = better fairness, moderate throughput (~600 TPS)
      const timePartition = Math.floor(now.getTime() / (30 * 1000)); // 30-second windows
      const messageGroupId = `time-partition-${timePartition}`;
      
      await sqs.publishMessage('orders-queue.fifo', event, messageGroupId);
      
      logger.info('Order created and event published', { 
        orderId: order.id,
        totalAmount: order.total_amount 
      });
    } catch (error) {
      logger.error('Failed to publish order event', { 
        orderId: order.id,
        error: error instanceof Error ? error.message : error 
      });
      // Don't fail the order creation if SQS fails
      // Production would use outbox pattern or retry mechanism
    }

    // Cache result for idempotency
    await redis.storeIdempotencyResult(fingerprint, order);

    return order;
  }

  async getOrderById(orderId: string): Promise<Order | null> {
    try {
      const result = await Database.query(
        `SELECT o.*, 
                json_agg(
                  json_build_object(
                    'product_id', oi.product_id,
                    'quantity', oi.quantity,
                    'unit_price', oi.unit_price
                  )
                ) as items
         FROM orders o
         LEFT JOIN order_items oi ON o.id = oi.order_id
         WHERE o.id = $1
         GROUP BY o.id, o.customer_id, o.status, o.total_amount, o.created_at, o.updated_at`,
        [orderId]
      );

      if (result.rows.length === 0) {
        return null;
      }

      const row = result.rows[0];
      return {
        id: row.id,
        customer_id: row.customer_id,
        status: row.status,
        total_amount: parseFloat(row.total_amount),
        items: row.items,
        created_at: row.created_at,
        updated_at: row.updated_at,
      };
    } catch (error) {
      logger.error('Failed to retrieve order', { 
        orderId,
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  // Mock product availability check for PoC
  // Production would check against product service/inventory
  private async checkProductAvailability(items: OrderItem[]): Promise<boolean> {
    // Simple mock - assume all products are available
    // Production would make API calls to product service
    return true;
  }
} 