import { v4 as uuidv4 } from 'uuid';
import { Database, sqs, logger } from '../../shared';
import { 
  Shipment, 
  OrderCreatedEvent, 
  OrderStatusUpdateEvent,
  Order 
} from '../../shared';

export class DeliveryService {
  // Simple delivery service for PoC
  // Production would have:
  // - Integration with real carriers (FedEx, UPS, etc.),
  // - Tracking number generation, real-time updates,
  // - Delivery optimization, route planning

  async processOrderCreated(event: OrderCreatedEvent): Promise<void> {
    try {
      const shipmentId = uuidv4();
      const now = new Date();

      // Create shipment record
      await Database.query(
        `INSERT INTO shipments (id, order_id, status, created_at, updated_at)
         VALUES ($1, $2, $3, $4, $5)`,
        [shipmentId, event.orderId, 'PROCESSING', now, now]
      );

      // Log delivery event
      await this.logDeliveryEvent(event.orderId, 'SHIPMENT_CREATED', {
        shipmentId,
        customerId: event.customerId,
        totalAmount: event.totalAmount,
      });

      logger.info('Shipment created for order', { 
        orderId: event.orderId, 
        shipmentId,
        customerId: event.customerId 
      });

      // Simulate initial processing delay
      // Production would integrate with warehouse management system
      setTimeout(async () => {
        await this.simulateShipmentProgress(shipmentId, event.orderId);
      }, 5000); // 5 second delay for demo

    } catch (error) {
      logger.error('Failed to process order created event', { 
        orderId: event.orderId,
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  async getShipmentByOrderId(orderId: string): Promise<Shipment | null> {
    try {
      const result = await Database.query(
        'SELECT * FROM shipments WHERE order_id = $1',
        [orderId]
      );

      if (result.rows.length === 0) {
        return null;
      }

      return result.rows[0];
    } catch (error) {
      logger.error('Failed to retrieve shipment', { 
        orderId,
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  async updateShipmentStatus(
    shipmentId: string, 
    status: 'PROCESSING' | 'SHIPPED' | 'DELIVERED',
    trackingNumber?: string,
    carrier?: string
  ): Promise<Shipment | null> {
    try {
      const now = new Date();
      const deliveredAt = status === 'DELIVERED' ? now : null;

      // Update shipment
      const result = await Database.query(
        `UPDATE shipments 
         SET status = $1, tracking_number = $2, carrier = $3, 
             delivered_at = $4, updated_at = $5
         WHERE id = $6
         RETURNING *`,
        [status, trackingNumber, carrier, deliveredAt, now, shipmentId]
      );

      if (result.rows.length === 0) {
        return null;
      }

      const shipment = result.rows[0];

      // Log delivery event
      await this.logDeliveryEvent(shipment.order_id, 'STATUS_UPDATED', {
        shipmentId,
        status,
        trackingNumber,
        carrier,
      });

      // Update order status and publish event
      await this.updateOrderStatus(shipment.order_id, status);

      return shipment;
    } catch (error) {
      logger.error('Failed to update shipment status', { 
        shipmentId,
        error: error instanceof Error ? error.message : error 
      });
      throw error;
    }
  }

  private async updateOrderStatus(orderId: string, deliveryStatus: string): Promise<void> {
    try {
      // Status mapping based on our design
      const STATUS_MAP: Record<string, Order['status']> = {
        'PROCESSING': 'PENDING_SHIPMENT',
        'SHIPPED': 'SHIPPED',
        'DELIVERED': 'DELIVERED',
      };

      const newOrderStatus = STATUS_MAP[deliveryStatus];
      if (!newOrderStatus) {
        logger.warn('Unknown delivery status for mapping', { deliveryStatus });
        return;
      }

      // Get current order status
      const orderResult = await Database.query(
        'SELECT status FROM orders WHERE id = $1',
        [orderId]
      );

      if (orderResult.rows.length === 0) {
        logger.error('Order not found for status update', { orderId });
        return;
      }

      const currentStatus = orderResult.rows[0].status;
      
      // Only update if status actually changed
      if (currentStatus === newOrderStatus) {
        logger.debug('Order status unchanged', { orderId, status: currentStatus });
        return;
      }

      // Update order status
      await Database.query(
        'UPDATE orders SET status = $1, updated_at = $2 WHERE id = $3',
        [newOrderStatus, new Date(), orderId]
      );

      // Publish status update event
      // Production would only publish for certain status changes
      const EVENTS_REQUIRED = ['SHIPPED', 'DELIVERED'];
      if (EVENTS_REQUIRED.includes(newOrderStatus)) {
        const event: OrderStatusUpdateEvent = {
          eventType: 'ORDER_STATUS_UPDATE',
          orderId,
          previousStatus: currentStatus,
          currentStatus: newOrderStatus,
          timestamp: new Date(),
        };

        // HYBRID FIFO: Time-partitioned ordering optimized for fairness
        // Status updates use same 30-second windows as order creation for consistency
        const timePartition = Math.floor(new Date().getTime() / (30 * 1000)); // 30-second windows
        const messageGroupId = `time-partition-${timePartition}`;
        
        await sqs.publishMessage('order-updates-queue.fifo', event, messageGroupId);
        
        logger.info('Order status updated and event published', { 
          orderId, 
          previousStatus: currentStatus, 
          newStatus: newOrderStatus 
        });
      }
    } catch (error) {
      logger.error('Failed to update order status', { 
        orderId,
        error: error instanceof Error ? error.message : error 
      });
      // Don't throw - shipment update should succeed even if order update fails
    }
  }

  private async logDeliveryEvent(
    orderId: string, 
    eventType: string, 
    details: any
  ): Promise<void> {
    try {
      await Database.query(
        `INSERT INTO delivery_events (order_id, event_type, details, created_at)
         VALUES ($1, $2, $3, $4)`,
        [orderId, eventType, JSON.stringify(details), new Date()]
      );
    } catch (error) {
      logger.error('Failed to log delivery event', { 
        orderId, 
        eventType, 
        error: error instanceof Error ? error.message : error 
      });
      // Don't throw - this is just for auditing
    }
  }

  // Simulate shipment progress for demo
  private async simulateShipmentProgress(shipmentId: string, orderId: string): Promise<void> {
    try {
      // Simulate shipping after 10 seconds
      setTimeout(async () => {
        await this.updateShipmentStatus(
          shipmentId, 
          'SHIPPED', 
          `TRK${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
          'Demo Carrier'
        );

        // Simulate delivery after another 15 seconds
        setTimeout(async () => {
          await this.updateShipmentStatus(shipmentId, 'DELIVERED');
        }, 15000);
      }, 10000);
    } catch (error) {
      logger.error('Failed to simulate shipment progress', { 
        shipmentId, 
        orderId,
        error: error instanceof Error ? error.message : error 
      });
    }
  }
} 