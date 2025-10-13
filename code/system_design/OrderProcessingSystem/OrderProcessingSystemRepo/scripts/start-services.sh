#!/bin/bash

# Order Processing System - Start Services Script
# This script builds and starts both Order Service and Delivery Service

set -e

echo "🚀 Starting Order Processing System Services"
echo "============================================="

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

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "Please run this script from the OrderProcessingSystemRepo directory"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is required but not installed"
    exit 1
fi

print_step "Step 1: Setting up environment..."

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        print_success "Created .env file from env.example"
    else
        print_error "env.example file not found"
        exit 1
    fi
else
    print_success ".env file already exists"
fi

print_step "Step 2: Installing dependencies..."

# Install npm dependencies
npm install
print_success "Dependencies installed"

print_step "Step 3: Building TypeScript..."

# Build TypeScript
npm run build
print_success "TypeScript compiled"

print_step "Step 4: Starting infrastructure services..."

# Start Docker Compose services (PostgreSQL, Redis, ElasticMQ)
docker-compose up -d postgres redis elasticmq
print_success "Infrastructure services started"

# Wait for services to be ready
print_warning "Waiting for services to be ready..."
sleep 10

print_step "Step 5: Setting up database..."

# Run database setup (if script exists)
if [ -f "scripts/setup-database.sh" ]; then
    ./scripts/setup-database.sh
    print_success "Database setup completed"
else
    print_warning "Database setup script not found - you may need to run database migrations manually"
fi

print_step "Step 6: Starting application services..."

# Start Order Service in background
print_warning "Starting Order Service on port 3001..."
SERVICE_NAME=order-service npm run start:order &
ORDER_SERVICE_PID=$!
print_success "Order Service started (PID: $ORDER_SERVICE_PID)"

# Wait a moment for Order Service to start
sleep 3

# Start Delivery Service in background
print_warning "Starting Delivery Service on port 3002..."
SERVICE_NAME=delivery-service npm run start:delivery &
DELIVERY_SERVICE_PID=$!
print_success "Delivery Service started (PID: $DELIVERY_SERVICE_PID)"

# Wait for services to be ready
print_warning "Waiting for services to be ready..."
sleep 5

print_step "Step 7: Checking service health..."

# Check Order Service health
if curl -s http://localhost:3001/health > /dev/null; then
    print_success "Order Service is healthy"
else
    print_error "Order Service health check failed"
fi

# Check Delivery Service health
if curl -s http://localhost:3002/health > /dev/null; then
    print_success "Delivery Service is healthy"
else
    print_error "Delivery Service health check failed"
fi

echo ""
print_success "🎉 Order Processing System is ready!"
echo ""
print_warning "Services running:"
echo "• Order Service: http://localhost:3001"
echo "• Delivery Service: http://localhost:3002"
echo "• PostgreSQL: localhost:5432"
echo "• Redis: localhost:6379"
echo "• ElasticMQ (SQS): http://localhost:9324"
echo ""
print_warning "Process IDs:"
echo "• Order Service: $ORDER_SERVICE_PID"
echo "• Delivery Service: $DELIVERY_SERVICE_PID"
echo ""
print_warning "To test the system:"
echo "• Run the demo: ./demo/demo.sh"
echo "• Use curl examples: see demo/curl-examples.md"
echo "• Check logs: docker-compose logs -f"
echo ""
print_warning "To stop services:"
echo "• Kill processes: kill $ORDER_SERVICE_PID $DELIVERY_SERVICE_PID"
echo "• Stop infrastructure: docker-compose down"
echo ""

# Create a stop script
cat > stop-services.sh << 'EOF'
#!/bin/bash
echo "Stopping Order Processing System..."

# Kill application services
if [ -n "$ORDER_SERVICE_PID" ]; then
    kill $ORDER_SERVICE_PID 2>/dev/null || true
fi

if [ -n "$DELIVERY_SERVICE_PID" ]; then
    kill $DELIVERY_SERVICE_PID 2>/dev/null || true
fi

# Stop Docker services
docker-compose down

echo "Services stopped."
EOF

chmod +x stop-services.sh
print_success "Created stop-services.sh script"

# Wait for user input to keep services running
echo ""
print_warning "Press Ctrl+C to stop all services..."
trap 'echo ""; print_warning "Stopping services..."; kill $ORDER_SERVICE_PID $DELIVERY_SERVICE_PID 2>/dev/null || true; docker-compose down; exit 0' INT

# Keep script running
while true; do
    sleep 1
done 