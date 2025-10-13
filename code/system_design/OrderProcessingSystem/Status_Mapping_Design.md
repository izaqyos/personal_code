# Status Mapping Design: Delivery ↔ Sales

## Overview

This document defines the explicit status mapping between the Delivery API and Sales API, ensuring consistent order state management across both systems.

## Sales API Order Statuses

| Status | Description | Customer Visible | Terminal |
|--------|-------------|------------------|----------|
| `PENDING_SHIPMENT` | Order created, awaiting shipment | ✅ | ❌ |
| `SHIPPED` | Order has been shipped | ✅ | ❌ |
| `IN_TRANSIT` | Order is in transit | ✅ | ❌ |
| `OUT_FOR_DELIVERY` | Order is out for delivery | ✅ | ❌ |
| `DELIVERED` | Order successfully delivered | ✅ | ✅ |
| `DELIVERY_FAILED` | Delivery attempt failed | ✅ | ❌ |
| `RETURNED` | Order returned to sender | ✅ | ✅ |
| `CANCELLED` | Order cancelled before shipping | ✅ | ✅ |

## Delivery API Statuses

| Status | Description | Internal Use | External Event |
|--------|-------------|--------------|----------------|
| `PICKUP_SCHEDULED` | Pickup from warehouse scheduled | ✅ | ❌ |
| `PICKED_UP` | Package picked up from warehouse | ✅ | ✅ |
| `IN_SORTING_FACILITY` | Package at sorting facility | ✅ | ❌ |
| `IN_TRANSIT_TO_DESTINATION` | Package in transit | ✅ | ✅ |
| `AT_LOCAL_FACILITY` | Package at local delivery facility | ✅ | ❌ |
| `OUT_FOR_DELIVERY` | Package out for delivery | ✅ | ✅ |
| `DELIVERY_ATTEMPTED` | Delivery attempt made | ✅ | ✅ |
| `DELIVERED` | Package delivered successfully | ✅ | ✅ |
| `DELIVERY_FAILED` | Delivery failed (multiple attempts) | ✅ | ✅ |
| `RETURN_TO_SENDER` | Package being returned | ✅ | ✅ |
| `RETURNED` | Package returned to sender | ✅ | ✅ |

## Status Mapping Table

| Delivery Status | Maps to Sales Status | Event Required | Notes |
|-----------------|---------------------|----------------|-------|
| `PICKUP_SCHEDULED` | `PENDING_SHIPMENT` | ❌ | No change needed |
| `PICKED_UP` | `SHIPPED` | ✅ | First shipping event |
| `IN_SORTING_FACILITY` | `SHIPPED` | ❌ | Maintain SHIPPED status |
| `IN_TRANSIT_TO_DESTINATION` | `IN_TRANSIT` | ✅ | Package moving |
| `AT_LOCAL_FACILITY` | `IN_TRANSIT` | ❌ | Maintain IN_TRANSIT status |
| `OUT_FOR_DELIVERY` | `OUT_FOR_DELIVERY` | ✅ | Final delivery phase |
| `DELIVERY_ATTEMPTED` | `OUT_FOR_DELIVERY` | ❌ | Maintain current status |
| `DELIVERED` | `DELIVERED` | ✅ | **Terminal state** |
| `DELIVERY_FAILED` | `DELIVERY_FAILED` | ✅ | After all attempts failed |
| `RETURN_TO_SENDER` | `RETURNED` | ✅ | Return process started |
| `RETURNED` | `RETURNED` | ✅ | **Terminal state** |

## Status Transition Rules

### Valid Transitions

```
PENDING_SHIPMENT → SHIPPED → IN_TRANSIT → OUT_FOR_DELIVERY → DELIVERED ✅
PENDING_SHIPMENT → SHIPPED → IN_TRANSIT → OUT_FOR_DELIVERY → DELIVERY_FAILED → RETURNED ✅
PENDING_SHIPMENT → CANCELLED ✅ (before shipping)
```

### Invalid Transitions

```
DELIVERED → any other status ❌ (terminal state)
RETURNED → any other status ❌ (terminal state)
CANCELLED → any other status ❌ (terminal state)
SHIPPED → PENDING_SHIPMENT ❌ (backwards transition)
```

## Event Schema

### Status Update Event

```typescript
interface DeliveryStatusUpdateEvent {
  eventType: 'DELIVERY_STATUS_UPDATE';
  orderId: string;
  deliveryId: string;
  deliveryStatus: DeliveryStatus;
  salesStatus: SalesOrderStatus;
  timestamp: Date;
  location?: {
    city: string;
    state: string;
    country: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
  };
  estimatedDelivery?: Date;
  metadata?: {
    trackingNumber: string;
    carrier: string;
    attemptNumber?: number;
    failureReason?: string;
  };
}
```

## Implementation Details

### 1. Status Mapping Service

```typescript
class StatusMappingService {
  private static readonly STATUS_MAP: Record<DeliveryStatus, SalesOrderStatus> = {
    PICKUP_SCHEDULED: 'PENDING_SHIPMENT',
    PICKED_UP: 'SHIPPED',
    IN_SORTING_FACILITY: 'SHIPPED',
    IN_TRANSIT_TO_DESTINATION: 'IN_TRANSIT',
    AT_LOCAL_FACILITY: 'IN_TRANSIT',
    OUT_FOR_DELIVERY: 'OUT_FOR_DELIVERY',
    DELIVERY_ATTEMPTED: 'OUT_FOR_DELIVERY',
    DELIVERED: 'DELIVERED',
    DELIVERY_FAILED: 'DELIVERY_FAILED',
    RETURN_TO_SENDER: 'RETURNED',
    RETURNED: 'RETURNED'
  };

  public static mapDeliveryToSalesStatus(deliveryStatus: DeliveryStatus): SalesOrderStatus {
    return this.STATUS_MAP[deliveryStatus];
  }

  public static isStatusUpdateRequired(currentSalesStatus: SalesOrderStatus, newDeliveryStatus: DeliveryStatus): boolean {
    const newSalesStatus = this.mapDeliveryToSalesStatus(newDeliveryStatus);
    return currentSalesStatus !== newSalesStatus;
  }

  public static isValidTransition(currentStatus: SalesOrderStatus, newStatus: SalesOrderStatus): boolean {
    const terminalStates = ['DELIVERED', 'RETURNED', 'CANCELLED'];
    
    // Cannot transition from terminal states
    if (terminalStates.includes(currentStatus)) {
      return false;
    }

    // Define valid transition paths
    const validTransitions: Record<SalesOrderStatus, SalesOrderStatus[]> = {
      PENDING_SHIPMENT: ['SHIPPED', 'CANCELLED'],
      SHIPPED: ['IN_TRANSIT', 'DELIVERED', 'RETURNED'],
      IN_TRANSIT: ['OUT_FOR_DELIVERY', 'DELIVERED', 'RETURNED'],
      OUT_FOR_DELIVERY: ['DELIVERED', 'DELIVERY_FAILED', 'RETURNED'],
      DELIVERY_FAILED: ['OUT_FOR_DELIVERY', 'RETURNED']
    };

    return validTransitions[currentStatus]?.includes(newStatus) || false;
  }
}
```

### 2. Event Processing Logic

```typescript
// In Delivery API - when status changes
async function publishStatusUpdate(deliveryId: string, newStatus: DeliveryStatus) {
  const delivery = await getDelivery(deliveryId);
  const salesStatus = StatusMappingService.mapDeliveryToSalesStatus(newStatus);
  
  // Only publish if status actually changes
  if (StatusMappingService.isStatusUpdateRequired(delivery.currentSalesStatus, newStatus)) {
    const event: DeliveryStatusUpdateEvent = {
      eventType: 'DELIVERY_STATUS_UPDATE',
      orderId: delivery.orderId,
      deliveryId: delivery.id,
      deliveryStatus: newStatus,
      salesStatus: salesStatus,
      timestamp: new Date(),
      location: delivery.currentLocation,
      estimatedDelivery: delivery.estimatedDeliveryDate,
      metadata: {
        trackingNumber: delivery.trackingNumber,
        carrier: delivery.carrier
      }
    };

    await publishEvent('order.status.updated', event);
  }
}

// In Sales API - event handler
async function handleDeliveryStatusUpdate(event: DeliveryStatusUpdateEvent) {
  const order = await getOrder(event.orderId);
  
  // Validate transition
  if (!StatusMappingService.isValidTransition(order.status, event.salesStatus)) {
    logger.error('Invalid status transition', {
      orderId: event.orderId,
      currentStatus: order.status,
      newStatus: event.salesStatus
    });
    return;
  }

  // Update order status
  await updateOrderStatus(event.orderId, {
    status: event.salesStatus,
    lastDeliveryUpdate: event.timestamp,
    trackingInfo: event.metadata,
    estimatedDelivery: event.estimatedDelivery
  });

  logger.info('Order status updated', {
    orderId: event.orderId,
    oldStatus: order.status,
    newStatus: event.salesStatus
  });
}
```

## Database Schema Updates

### Sales API - Orders Table

```sql
-- Add tracking and delivery fields
ALTER TABLE orders ADD COLUMN tracking_number VARCHAR(255);
ALTER TABLE orders ADD COLUMN carrier VARCHAR(100);
ALTER TABLE orders ADD COLUMN estimated_delivery_date TIMESTAMP;
ALTER TABLE orders ADD COLUMN last_delivery_update TIMESTAMP;

-- Add status transition history
CREATE TABLE order_status_history (
  id SERIAL PRIMARY KEY,
  order_id UUID REFERENCES orders(id),
  old_status VARCHAR(50),
  new_status VARCHAR(50) NOT NULL,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  changed_by VARCHAR(100), -- 'system', 'delivery_api', etc.
  metadata JSONB
);

CREATE INDEX idx_order_status_history_order_id ON order_status_history(order_id);
CREATE INDEX idx_order_status_history_changed_at ON order_status_history(changed_at);
```

### Delivery API - Add Sales Status Tracking

```sql
-- Track what status was sent to Sales API
ALTER TABLE deliveries ADD COLUMN current_sales_status VARCHAR(50);
ALTER TABLE deliveries ADD COLUMN last_status_sync TIMESTAMP;
```

## Error Handling

### Retry Logic for Failed Status Updates

```typescript
class StatusUpdateService {
  async updateOrderStatusWithRetry(orderId: string, statusUpdate: StatusUpdate, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        await this.updateOrderStatus(orderId, statusUpdate);
        return;
      } catch (error) {
        logger.warn(`Status update attempt ${attempt} failed`, {
          orderId,
          error: error.message,
          attempt
        });

        if (attempt === maxRetries) {
          // Store failed update for manual reconciliation
          await this.storeFailedStatusUpdate(orderId, statusUpdate, error);
          throw new Error(`Status update failed after ${maxRetries} attempts`);
        }

        // Exponential backoff
        await this.delay(Math.pow(2, attempt) * 1000);
      }
    }
  }
}
```

## Monitoring and Alerting

### Key Metrics to Track

1. **Status Update Latency**: Time between delivery status change and sales status update
2. **Failed Status Updates**: Count of failed status synchronization attempts
3. **Invalid Transitions**: Count of invalid status transition attempts
4. **Status Drift**: Orders where delivery and sales statuses are out of sync

### Reconciliation Process

```typescript
// Daily reconciliation job
async function reconcileOrderStatuses() {
  const inconsistentOrders = await findOrdersWithStatusMismatch();
  
  for (const order of inconsistentOrders) {
    const deliveryStatus = await getDeliveryStatus(order.deliveryId);
    const expectedSalesStatus = StatusMappingService.mapDeliveryToSalesStatus(deliveryStatus);
    
    if (order.status !== expectedSalesStatus) {
      logger.warn('Status mismatch detected', {
        orderId: order.id,
        currentSalesStatus: order.status,
        expectedSalesStatus,
        deliveryStatus
      });
      
      // Auto-correct if valid transition
      if (StatusMappingService.isValidTransition(order.status, expectedSalesStatus)) {
        await this.updateOrderStatus(order.id, { status: expectedSalesStatus });
      }
    }
  }
}
```

## Testing Strategy

### Unit Tests
- Status mapping logic
- Transition validation
- Event schema validation

### Integration Tests
- End-to-end status flow
- Event publishing and consumption
- Error handling and retry logic

### Load Tests
- High-volume status updates
- Event processing performance
- Database performance under load

This status mapping design ensures reliable, consistent, and auditable order status management across both systems while providing clear error handling and monitoring capabilities. 