#!/bin/bash

# Order Processing System Demo Script
# This script demonstrates the complete order flow using curl commands

set -e

echo "🚀 Order Processing System Demo"
echo "================================="
echo ""

# Configuration
ORDER_SERVICE_URL="http://localhost:3001"
DELIVERY_SERVICE_URL="http://localhost:3002"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to make HTTP requests with error handling
make_request() {
    local method=$1
    local url=$2
    local data=$3
    local headers=$4
    
    if [ -n "$headers" ]; then
        response=$(curl -s -X $method "$url" -H "$headers" -H "Content-Type: application/json" -d "$data" -w "HTTPSTATUS:%{http_code}")
    else
        response=$(curl -s -X $method "$url" -H "Content-Type: application/json" -d "$data" -w "HTTPSTATUS:%{http_code}")
    fi
    
    http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
    body=$(echo $response | sed -e 's/HTTPSTATUS\:.*//g')
    
    if [ $http_code -lt 200 ] || [ $http_code -gt 299 ]; then
        print_error "HTTP $http_code: $body"
        return 1
    fi
    
    echo "$body"
    return 0
}

# Step 1: Check health of both services
print_step "Step 1: Checking service health..."
echo ""

echo "Checking Order Service health:"
if health_response=$(make_request GET "$ORDER_SERVICE_URL/health"); then
    print_success "Order Service is healthy"
    echo "$health_response" | jq '.'
else
    print_error "Order Service is not healthy"
    exit 1
fi

echo ""
echo "Checking Delivery Service health:"
if health_response=$(make_request GET "$DELIVERY_SERVICE_URL/health"); then
    print_success "Delivery Service is healthy"
    echo "$health_response" | jq '.'
else
    print_error "Delivery Service is not healthy"
    exit 1
fi

echo ""
echo "Press Enter to continue..."
read

# Step 2: Get JWT token
print_step "Step 2: Getting JWT token..."
echo ""

token_request='{
    "client_id": "demo-client",
    "client_secret": "demo-secret",
    "grant_type": "client_credentials"
}'

if token_response=$(make_request POST "$ORDER_SERVICE_URL/auth/token" "$token_request"); then
    access_token=$(echo "$token_response" | jq -r '.access_token')
    print_success "JWT token obtained"
    echo "$token_response" | jq '.'
    echo ""
    print_warning "Token (first 50 chars): ${access_token:0:50}..."
else
    print_error "Failed to get JWT token"
    exit 1
fi

echo ""
echo "Press Enter to continue..."
read

# Step 3: Create an order
print_step "Step 3: Creating a new order..."
echo ""

order_request='{
    "customer_id": "customer-demo-001",
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
}'

auth_header="Authorization: Bearer $access_token"

if order_response=$(make_request POST "$ORDER_SERVICE_URL/orders" "$order_request" "$auth_header"); then
    order_id=$(echo "$order_response" | jq -r '.order_id')
    print_success "Order created successfully"
    echo "$order_response" | jq '.'
    echo ""
    print_warning "Order ID: $order_id"
else
    print_error "Failed to create order"
    exit 1
fi

echo ""
echo "Press Enter to continue..."
read

# Step 4: Retrieve the order
print_step "Step 4: Retrieving the order..."
echo ""

if order_details=$(make_request GET "$ORDER_SERVICE_URL/orders/$order_id" "" "$auth_header"); then
    print_success "Order retrieved successfully"
    echo "$order_details" | jq '.'
else
    print_error "Failed to retrieve order"
    exit 1
fi

echo ""
echo "Press Enter to continue..."
read

# Step 5: Wait for shipment creation and check delivery service
print_step "Step 5: Checking shipment status..."
echo ""

print_warning "Waiting for delivery service to process the order..."
sleep 3

if shipment_response=$(make_request GET "$DELIVERY_SERVICE_URL/delivery/shipment/$order_id"); then
    shipment_id=$(echo "$shipment_response" | jq -r '.id')
    print_success "Shipment found"
    echo "$shipment_response" | jq '.'
    echo ""
    print_warning "Shipment ID: $shipment_id"
else
    print_error "Shipment not found yet"
    shipment_id=""
fi

echo ""
echo "Press Enter to continue..."
read

# Step 6: Simulate shipment status updates
if [ -n "$shipment_id" ]; then
    print_step "Step 6: Simulating shipment status updates..."
    echo ""
    
    # Update to SHIPPED
    print_warning "Updating shipment to SHIPPED status..."
    shipped_request='{
        "status": "SHIPPED",
        "tracking_number": "TRK123456789",
        "carrier": "Demo Express"
    }'
    
    if shipped_response=$(make_request POST "$DELIVERY_SERVICE_URL/delivery/shipment/$shipment_id/status" "$shipped_request"); then
        print_success "Shipment updated to SHIPPED"
        echo "$shipped_response" | jq '.'
    else
        print_error "Failed to update shipment to SHIPPED"
    fi
    
    echo ""
    echo "Press Enter to continue..."
    read
    
    # Update to DELIVERED
    print_warning "Updating shipment to DELIVERED status..."
    delivered_request='{
        "status": "DELIVERED"
    }'
    
    if delivered_response=$(make_request POST "$DELIVERY_SERVICE_URL/delivery/shipment/$shipment_id/status" "$delivered_request"); then
        print_success "Shipment updated to DELIVERED"
        echo "$delivered_response" | jq '.'
    else
        print_error "Failed to update shipment to DELIVERED"
    fi
    
    echo ""
    echo "Press Enter to continue..."
    read
fi

# Step 7: Check final order status
print_step "Step 7: Checking final order status..."
echo ""

if final_order=$(make_request GET "$ORDER_SERVICE_URL/orders/$order_id" "" "$auth_header"); then
    final_status=$(echo "$final_order" | jq -r '.status')
    print_success "Final order status: $final_status"
    echo "$final_order" | jq '.'
else
    print_error "Failed to retrieve final order status"
fi

echo ""
print_step "Demo completed! 🎉"
echo ""
print_warning "Key points demonstrated:"
echo "• JWT authentication with client credentials flow"
echo "• Order creation with validation"
echo "• Asynchronous processing via SQS"
echo "• Shipment creation and status updates"
echo "• Order status synchronization"
echo "• Health check endpoints"
echo ""
print_warning "The system automatically simulates shipment progress:"
echo "• PROCESSING → SHIPPED (after 10 seconds)"
echo "• SHIPPED → DELIVERED (after 25 seconds total)"
echo ""
print_success "Demo script completed successfully!" 