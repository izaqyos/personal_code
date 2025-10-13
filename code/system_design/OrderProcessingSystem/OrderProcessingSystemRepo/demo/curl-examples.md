# Order Processing System - API Examples

This document contains curl examples for testing the Order Processing System APIs.

## Prerequisites

1. Make sure both services are running:
   - Order Service: `http://localhost:3001`
   - Delivery Service: `http://localhost:3002`

2. Install `jq` for JSON formatting (optional but recommended):
   ```bash
   brew install jq  # macOS
   sudo apt-get install jq  # Ubuntu
   ```

## 1. Health Checks

### Order Service Health
```bash
curl -s http://localhost:3001/health | jq '.'
```

### Delivery Service Health
```bash
curl -s http://localhost:3002/health | jq '.'
```

## 2. Authentication

### Get JWT Token
```bash
curl -s -X POST http://localhost:3001/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "demo-client",
    "client_secret": "demo-secret",
    "grant_type": "client_credentials"
  }' | jq '.'
```

### Store Token in Variable
```bash
TOKEN=$(curl -s -X POST http://localhost:3001/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "demo-client",
    "client_secret": "demo-secret",
    "grant_type": "client_credentials"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### Verify Token (Introspection)
```bash
curl -s -X POST http://localhost:3001/auth/introspect \
  -H "Content-Type: application/json" \
  -d "{\"token\": \"$TOKEN\"}" | jq '.'
```

## 3. Order Management

### Create Order
```bash
curl -s -X POST http://localhost:3001/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-001",
    "items": [
      {
        "product_id": "laptop-001",
        "quantity": 1,
        "unit_price": 999.99
      },
      {
        "product_id": "mouse-001",
        "quantity": 2,
        "unit_price": 29.99
      }
    ]
  }' | jq '.'
```

### Store Order ID
```bash
ORDER_ID=$(curl -s -X POST http://localhost:3001/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-002",
    "items": [
      {
        "product_id": "keyboard-001",
        "quantity": 1,
        "unit_price": 79.99
      }
    ]
  }' | jq -r '.order_id')

echo "Order ID: $ORDER_ID"
```

### Get Order by ID
```bash
curl -s -X GET http://localhost:3001/orders/$ORDER_ID \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

## 4. Delivery Management

### Get Shipment by Order ID
```bash
curl -s -X GET http://localhost:3002/delivery/shipment/$ORDER_ID | jq '.'
```

### Store Shipment ID
```bash
SHIPMENT_ID=$(curl -s -X GET http://localhost:3002/delivery/shipment/$ORDER_ID | jq -r '.id')
echo "Shipment ID: $SHIPMENT_ID"
```

### Update Shipment Status to SHIPPED
```bash
curl -s -X POST http://localhost:3002/delivery/shipment/$SHIPMENT_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "SHIPPED",
    "tracking_number": "TRK123456789",
    "carrier": "Demo Express"
  }' | jq '.'
```

### Update Shipment Status to DELIVERED
```bash
curl -s -X POST http://localhost:3002/delivery/shipment/$SHIPMENT_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "DELIVERED"
  }' | jq '.'
```

## 5. Complete Flow Example

Here's a complete example that demonstrates the entire flow:

```bash
#!/bin/bash

# Get JWT token
TOKEN=$(curl -s -X POST http://localhost:3001/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "demo-client",
    "client_secret": "demo-secret",
    "grant_type": "client_credentials"
  }' | jq -r '.access_token')

echo "1. Token obtained: ${TOKEN:0:50}..."

# Create order
ORDER_RESPONSE=$(curl -s -X POST http://localhost:3001/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer-demo",
    "items": [
      {
        "product_id": "demo-product",
        "quantity": 1,
        "unit_price": 99.99
      }
    ]
  }')

ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.order_id')
echo "2. Order created: $ORDER_ID"

# Wait for shipment creation
echo "3. Waiting for shipment creation..."
sleep 5

# Get shipment
SHIPMENT_RESPONSE=$(curl -s -X GET http://localhost:3002/delivery/shipment/$ORDER_ID)
SHIPMENT_ID=$(echo "$SHIPMENT_RESPONSE" | jq -r '.id')
echo "4. Shipment found: $SHIPMENT_ID"

# Update to shipped
echo "5. Updating to SHIPPED..."
curl -s -X POST http://localhost:3002/delivery/shipment/$SHIPMENT_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "SHIPPED",
    "tracking_number": "TRK999888777",
    "carrier": "Fast Delivery"
  }' | jq '.'

# Check final order status
echo "6. Final order status:"
curl -s -X GET http://localhost:3001/orders/$ORDER_ID \
  -H "Authorization: Bearer $TOKEN" | jq '.status'
```

## 6. Error Scenarios

### Invalid Authentication
```bash
curl -s -X GET http://localhost:3001/orders/some-id \
  -H "Authorization: Bearer invalid-token" | jq '.'
```

### Missing Authorization Header
```bash
curl -s -X GET http://localhost:3001/orders/some-id | jq '.'
```

### Invalid Order Data
```bash
curl -s -X POST http://localhost:3001/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "",
    "items": []
  }' | jq '.'
```

### Non-existent Order
```bash
curl -s -X GET http://localhost:3001/orders/non-existent-id \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```

## 7. Load Testing Example

For basic load testing, you can use a simple loop:

```bash
#!/bin/bash

# Get token once
TOKEN=$(curl -s -X POST http://localhost:3001/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "demo-client",
    "client_secret": "demo-secret",
    "grant_type": "client_credentials"
  }' | jq -r '.access_token')

# Create 10 orders
for i in {1..10}; do
  echo "Creating order $i..."
  curl -s -X POST http://localhost:3001/orders \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"customer_id\": \"customer-$i\",
      \"items\": [
        {
          \"product_id\": \"product-$i\",
          \"quantity\": 1,
          \"unit_price\": 19.99
        }
      ]
    }" | jq -r '.order_id'
done
```

## Notes

- Replace `localhost` with your actual host if running remotely
- JWT tokens expire after 24 hours by default
- The system automatically simulates shipment progress after order creation
- Check the service logs for detailed processing information 