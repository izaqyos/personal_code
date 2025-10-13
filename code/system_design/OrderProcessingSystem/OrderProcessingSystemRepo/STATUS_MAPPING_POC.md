# PoC Status Mapping: Simplified Order Flow

## Overview
This document defines a simple status mapping for PoC implementation, following the KISS principle. A more comprehansive status model (8 order statuses, 11 delivery statuses) can be implemented later for production.

## PoC Order Statuses (Order Service)

| Status | Description | Customer Visible | Terminal |
|--------|-------------|------------------|----------|
| `PENDING_SHIPMENT` | Order created, awaiting shipment | ✅ | ❌ |
| `SHIPPED` | Order has been shipped | ✅ | ❌ |
| `DELIVERED` | Order successfully delivered | ✅ | ✅ |

## PoC Delivery Statuses (Delivery Service)

| Status | Description | Maps to Order Status |
|--------|-------------|---------------------|
| `PROCESSING` | Shipment being prepared | `PENDING_SHIPMENT` |
| `SHIPPED` | Package shipped from warehouse | `SHIPPED` |
| `DELIVERED` | Package delivered to customer | `DELIVERED` |

## Simplified Flow

```
Order Created → PENDING_SHIPMENT
    ↓
Delivery Processing → PROCESSING (no status change)
    ↓
Package Shipped → SHIPPED
    ↓
Package Delivered → DELIVERED (terminal)
```

## Status Mapping Logic

```typescript
// Maps Delivery Service statuses → Order Service statuses
// Key: Delivery status (internal), Value: Order status (customer-visible)
const STATUS_MAP = {
  'PROCESSING': 'PENDING_SHIPMENT',  // No change needed
  'SHIPPED': 'SHIPPED',              // Update required
  'DELIVERED': 'DELIVERED'           // Update required
};

// Determines whether delivery status change should trigger event/notification
// Key: Delivery status, Value: Boolean - whether to publish event to Order Service
const EVENTS_REQUIRED = {
  'PROCESSING': false,   // Internal delivery status
  'SHIPPED': true,       // Customer notification needed
  'DELIVERED': true      // Customer notification needed
};
```

## Event Schema (Simplified)

```typescript
interface OrderStatusUpdateEvent {
  eventType: 'ORDER_STATUS_UPDATE';
  orderId: string;
  previousStatus: 'PENDING_SHIPMENT' | 'SHIPPED' | 'DELIVERED';
  currentStatus: 'PENDING_SHIPMENT' | 'SHIPPED' | 'DELIVERED';
  timestamp: Date;
  trackingNumber?: string;
  carrier?: string;
}
```

## Database Schema

<!-- Note: Lines below only show status constraints, not full table schema -->
<!-- Full schema includes id (UUID PK), customer_id, total_amount, timestamps, etc. -->

### Orders Table
```sql
status VARCHAR(50) NOT NULL CHECK (status IN ('PENDING_SHIPMENT', 'SHIPPED', 'DELIVERED'))
```

### Shipments Table
```sql
status VARCHAR(50) NOT NULL CHECK (status IN ('PROCESSING', 'SHIPPED', 'DELIVERED'))
```

## Production Migration Path

When moving to production, we can extend this model to include:
- `IN_TRANSIT`, `OUT_FOR_DELIVERY` (customer visibility)
- `DELIVERY_FAILED`, `RETURNED`, `CANCELLED` (error handling)
- More granular delivery statuses for tracking

This PoC approach reduces complexity while proving the core order processing flow. 