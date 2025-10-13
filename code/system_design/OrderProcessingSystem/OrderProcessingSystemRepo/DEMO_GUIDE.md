# Order Processing System - Demo Guide

## 🎮 Interactive Demo Walkthrough

This guide demonstrates a complete end-to-end order processing flow using the Order Processing System.

## Prerequisites

Ensure the system is running:
```bash
./scripts/manage-system.sh up
./scripts/health-check.sh  # Verify all services are healthy
```

## Demo Execution

### Step 1: Start the Demo

```bash
./scripts/manage-system.sh demo
```

**Expected Output:**
```
=============================================
🎮 Order Processing System - Interactive Demo
=============================================
Welcome to the Order Processing System Demo!

This demo will walk you through:
1. Creating a new order
2. Processing the order through delivery
3. Tracking status updates
4. Viewing the complete order lifecycle

Press Enter to continue...
```

### Step 2: Create a New Order

**Demo Action:** Creates a new order with sample products

**API Call:**
```bash
curl -X POST http://localhost:3001/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "customerId": "demo-customer-001",
    "items": [
      {
        "productId": "laptop-001",
        "quantity": 1,
        "unitPrice": 999.99
      },
      {
        "productId": "mouse-001", 
        "quantity": 2,
        "unitPrice": 29.99
      }
    ]
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "orderId": "ord_1234567890abcdef",
  "status": "PENDING_SHIPMENT",
  "customerId": "demo-customer-001",
  "totalAmount": 1059.97,
  "items": [
    {
      "id": 1,
      "productId": "laptop-001",
      "quantity": 1,
      "unitPrice": 999.99
    },
    {
      "id": 2,
      "productId": "mouse-001",
      "quantity": 2,
      "unitPrice": 29.99
    }
  ],
  "createdAt": "2025-07-12T16:30:00.000Z",
  "message": "Order created successfully and queued for processing"
}
```

**System Activities:**
- ✅ Order saved to PostgreSQL database
- ✅ Order details sent to SQS queue (`orders-queue.fifo`)
- ✅ JWT authentication validated
- ✅ Idempotency key stored in Redis

### Step 3: Automatic Delivery Processing

**Demo Action:** Delivery service automatically picks up the order from SQS

**Console Output:**
```
🚚 Delivery Service Processing...

[2025-07-12T16:30:05.123Z] INFO: Received order from SQS
{
  "orderId": "ord_1234567890abcdef",
  "customerId": "demo-customer-001",
  "totalAmount": 1059.97,
  "items": 2
}

[2025-07-12T16:30:05.456Z] INFO: Creating shipment record
{
  "shipmentId": "shp_abcdef1234567890",
  "orderId": "ord_1234567890abcdef",
  "status": "PROCESSING",
  "trackingNumber": "TRK-2025071200001"
}

[2025-07-12T16:30:06.789Z] INFO: Shipment created successfully
```

**Database Updates:**
- ✅ Order status updated to `PROCESSING`
- ✅ Shipment record created
- ✅ Delivery event logged

### Step 4: Track Order Status

**Demo Action:** Query order status to see processing updates

**API Call:**
```bash
curl -X GET http://localhost:3001/api/orders/ord_1234567890abcdef \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
{
  "success": true,
  "order": {
    "id": "ord_1234567890abcdef",
    "customerId": "demo-customer-001",
    "status": "PROCESSING",
    "totalAmount": 1059.97,
    "createdAt": "2025-07-12T16:30:00.000Z",
    "updatedAt": "2025-07-12T16:30:06.000Z",
    "items": [
      {
        "id": 1,
        "productId": "laptop-001",
        "quantity": 1,
        "unitPrice": 999.99
      },
      {
        "id": 2,
        "productId": "mouse-001",
        "quantity": 2,
        "unitPrice": 29.99
      }
    ],
    "shipment": {
      "id": "shp_abcdef1234567890",
      "status": "PROCESSING",
      "trackingNumber": "TRK-2025071200001",
      "carrier": "DemoShip Express",
      "createdAt": "2025-07-12T16:30:05.000Z"
    }
  }
}
```

### Step 5: Simulate Delivery Status Updates

**Demo Action:** Delivery service processes status updates

**Console Output:**
```
📦 Simulating Delivery Status Updates...

[2025-07-12T16:30:15.123Z] INFO: Shipment status update
{
  "shipmentId": "shp_abcdef1234567890",
  "status": "SHIPPED",
  "trackingNumber": "TRK-2025071200001",
  "carrier": "DemoShip Express"
}

[2025-07-12T16:30:25.456Z] INFO: Shipment status update
{
  "shipmentId": "shp_abcdef1234567890",
  "status": "OUT_FOR_DELIVERY",
  "trackingNumber": "TRK-2025071200001"
}

[2025-07-12T16:30:35.789Z] INFO: Shipment status update
{
  "shipmentId": "shp_abcdef1234567890",
  "status": "DELIVERED",
  "trackingNumber": "TRK-2025071200001",
  "deliveredAt": "2025-07-12T16:30:35.000Z"
}
```

### Step 6: Final Order Status

**Demo Action:** Check final order status

**API Call:**
```bash
curl -X GET http://localhost:3001/api/orders/ord_1234567890abcdef \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
{
  "success": true,
  "order": {
    "id": "ord_1234567890abcdef",
    "customerId": "demo-customer-001",
    "status": "DELIVERED",
    "totalAmount": 1059.97,
    "createdAt": "2025-07-12T16:30:00.000Z",
    "updatedAt": "2025-07-12T16:30:35.000Z",
    "items": [
      {
        "id": 1,
        "productId": "laptop-001",
        "quantity": 1,
        "unitPrice": 999.99
      },
      {
        "id": 2,
        "productId": "mouse-001",
        "quantity": 2,
        "unitPrice": 29.99
      }
    ],
    "shipment": {
      "id": "shp_abcdef1234567890",
      "status": "DELIVERED",
      "trackingNumber": "TRK-2025071200001",
      "carrier": "DemoShip Express",
      "createdAt": "2025-07-12T16:30:05.000Z",
      "deliveredAt": "2025-07-12T16:30:35.000Z"
    },
    "deliveryEvents": [
      {
        "id": 1,
        "eventType": "ORDER_RECEIVED",
        "details": {"source": "order-service"},
        "createdAt": "2025-07-12T16:30:05.000Z"
      },
      {
        "id": 2,
        "eventType": "SHIPMENT_CREATED",
        "details": {"trackingNumber": "TRK-2025071200001"},
        "createdAt": "2025-07-12T16:30:05.000Z"
      },
      {
        "id": 3,
        "eventType": "STATUS_UPDATE",
        "details": {"status": "SHIPPED"},
        "createdAt": "2025-07-12T16:30:15.000Z"
      },
      {
        "id": 4,
        "eventType": "STATUS_UPDATE",
        "details": {"status": "OUT_FOR_DELIVERY"},
        "createdAt": "2025-07-12T16:30:25.000Z"
      },
      {
        "id": 5,
        "eventType": "STATUS_UPDATE",
        "details": {"status": "DELIVERED"},
        "createdAt": "2025-07-12T16:30:35.000Z"
      }
    ]
  }
}
```

## Demo Summary

**Successful Demo Completion:**
```
=============================================
🎉 Demo Completed Successfully!
=============================================

Order Processing Flow Summary:
✅ Order Created: ord_1234567890abcdef
✅ JWT Authentication: Validated
✅ Database Storage: PostgreSQL
✅ Message Queue: SQS (orders-queue.fifo)
✅ Delivery Processing: Automatic
✅ Status Updates: Real-time
✅ Final Status: DELIVERED

System Components Tested:
✅ Order Service (Port 3001)
✅ Delivery Service (Port 3002)
✅ PostgreSQL Database
✅ Redis Cache (Idempotency)
✅ ElasticMQ (SQS)
✅ JWT Authentication
✅ Error Handling
✅ Logging & Monitoring

Performance Metrics:
• Order Creation: ~200ms
• Queue Processing: ~1s
• Status Updates: ~100ms each
• Total Flow Time: ~35s

Next Steps:
• View logs: ./scripts/manage-system.sh logs
• Check health: ./scripts/health-check.sh
• Stop system: ./scripts/manage-system.sh down
```

## Architecture Validation

The demo validates the following architectural components:

### 🔐 **Security**
- JWT token authentication on all endpoints
- Input validation and sanitization
- SQL injection protection

### 🚀 **Performance**
- Asynchronous message processing
- Database connection pooling
- Redis caching for idempotency

### 🔄 **Reliability**
- Message queue durability (FIFO queues)
- Database transactions
- Error handling and retry logic

### 📊 **Monitoring**
- Structured logging (JSON format)
- Health check endpoints
- Delivery event audit trail

### 🏗️ **Scalability**
- Microservices architecture
- Stateless service design
- Queue-based decoupling

## Troubleshooting

If the demo fails:

1. **Check system health:**
   ```bash
   ./scripts/health-check.sh
   ```

2. **Verify services are running:**
   ```bash
   ./scripts/manage-system.sh status
   ```

3. **Check logs:**
   ```bash
   ./scripts/manage-system.sh logs
   ```

4. **Restart if needed:**
   ```bash
   ./scripts/manage-system.sh restart
   ```

## Manual Testing

You can also test individual components manually:

### Create Order (Manual)
```bash
curl -X POST http://localhost:3001/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(node -e "console.log(require('jsonwebtoken').sign({userId: 'demo-user'}, 'dev-secret-key-change-in-production'))")" \
  -d '{
    "customerId": "manual-test-001",
    "items": [
      {"productId": "test-product", "quantity": 1, "unitPrice": 99.99}
    ]
  }'
```

### Check Health
```bash
curl http://localhost:3001/health | jq .
curl http://localhost:3002/health | jq .
```

### View Database
```bash
PGPASSWORD=admin123 psql -h localhost -p 5432 -U admin -d orderprocessing -c "SELECT * FROM orders ORDER BY created_at DESC LIMIT 5;"
```

This completes the comprehensive demo guide showing successful order processing from creation to delivery! 