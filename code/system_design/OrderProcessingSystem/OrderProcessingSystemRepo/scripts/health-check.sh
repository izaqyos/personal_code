#!/bin/bash

# Order Processing System - Comprehensive Health Check Script
# This script performs a complete system inspection

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${CYAN}=============================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}=============================================${NC}"
}

print_section() {
    echo -e "${BLUE}--- $1 ---${NC}"
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

print_header "🏥 Order Processing System - Health Inspection"
echo "Timestamp: $(date)"
echo ""

# =============================================================================
print_section "1. DOCKER INFRASTRUCTURE STATUS"
# =============================================================================

echo "Docker Compose Services:"
docker-compose ps 2>/dev/null || echo "No docker-compose services found"

echo ""
echo "Docker Container Details:"
docker ps --filter "name=order-processing" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "No containers found"

echo ""
echo "Docker Service Logs (last 10 lines each):"
echo "--- PostgreSQL ---"
docker-compose logs --tail=10 postgres 2>/dev/null || echo "PostgreSQL logs not available"

echo "--- Redis ---"
docker-compose logs --tail=10 redis 2>/dev/null || echo "Redis logs not available"

echo "--- ElasticMQ ---"
docker-compose logs --tail=10 elasticmq 2>/dev/null || echo "ElasticMQ logs not available"

# =============================================================================
print_section "2. PORT USAGE INSPECTION"
# =============================================================================

echo "Critical Ports Status:"
echo "Port 3001 (Order Service):"
lsof -i :3001 2>/dev/null || echo "  Port 3001 is free"

echo "Port 3002 (Delivery Service):"
lsof -i :3002 2>/dev/null || echo "  Port 3002 is free"

echo "Port 5432 (PostgreSQL):"
lsof -i :5432 2>/dev/null || echo "  Port 5432 is free"

echo "Port 6379 (Redis):"
lsof -i :6379 2>/dev/null || echo "  Port 6379 is free"

echo "Port 9324 (ElasticMQ):"
lsof -i :9324 2>/dev/null || echo "  Port 9324 is free"

# =============================================================================
print_section "3. APPLICATION SERVICES STATUS"
# =============================================================================

echo "Process Status:"
if [ -f ".order-service.pid" ]; then
    ORDER_PID=$(cat .order-service.pid)
    if ps -p "$ORDER_PID" > /dev/null 2>&1; then
        print_success "Order Service running (PID: $ORDER_PID)"
    else
        print_error "Order Service PID file exists but process not running"
    fi
else
    print_warning "Order Service PID file not found"
fi

if [ -f ".delivery-service.pid" ]; then
    DELIVERY_PID=$(cat .delivery-service.pid)
    if ps -p "$DELIVERY_PID" > /dev/null 2>&1; then
        print_success "Delivery Service running (PID: $DELIVERY_PID)"
    else
        print_error "Delivery Service PID file exists but process not running"
    fi
else
    print_warning "Delivery Service PID file not found"
fi

echo ""
echo "Health Endpoint Tests:"
echo "Order Service Health:"
if curl -s http://localhost:3001/health > /dev/null 2>&1; then
    print_success "Order Service health check passed"
    curl -s http://localhost:3001/health | jq . 2>/dev/null || curl -s http://localhost:3001/health
else
    print_error "Order Service health check failed"
fi

echo ""
echo "Delivery Service Health:"
if curl -s http://localhost:3002/health > /dev/null 2>&1; then
    print_success "Delivery Service health check passed"
    curl -s http://localhost:3002/health | jq . 2>/dev/null || curl -s http://localhost:3002/health
else
    print_error "Delivery Service health check failed"
fi

# =============================================================================
print_section "4. DATABASE INSPECTION"
# =============================================================================

echo "Database Connection Test:"
if PGPASSWORD=admin123 psql -h localhost -p 5432 -U admin -d orderprocessing -c "SELECT 1;" > /dev/null 2>&1; then
    print_success "Database connection successful"
    DB_USER="admin"
    DB_PASSWORD="admin123"
    DB_NAME="orderprocessing"
else
    print_error "Database connection failed with admin/orderprocessing"
    echo "Trying alternative credentials..."
    if PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -d order_processing -c "SELECT 1;" > /dev/null 2>&1; then
        print_success "Database connection successful (alternative credentials)"
        DB_USER="postgres"
        DB_PASSWORD="postgres"
        DB_NAME="order_processing"
    else
        print_error "All database connection attempts failed"
        DB_USER="admin"
        DB_PASSWORD="admin123"
        DB_NAME="orderprocessing"
    fi
fi

# Use discovered or default credentials
DB_USER=${DB_USER:-admin}
DB_PASSWORD=${DB_PASSWORD:-admin123}
DB_NAME=${DB_NAME:-orderprocessing}

echo ""
echo "Database Tables:"
PGPASSWORD=$DB_PASSWORD psql -h localhost -p 5432 -U $DB_USER -d $DB_NAME -c "\dt" 2>/dev/null || echo "Could not list tables"

echo ""
echo "Table Row Counts:"
PGPASSWORD=$DB_PASSWORD psql -h localhost -p 5432 -U $DB_USER -d $DB_NAME -c "
SELECT 
    'orders' as table_name, COUNT(*) as row_count FROM orders
UNION ALL
SELECT 
    'order_items' as table_name, COUNT(*) as row_count FROM order_items
UNION ALL
SELECT 
    'shipments' as table_name, COUNT(*) as row_count FROM shipments
UNION ALL
SELECT 
    'delivery_events' as table_name, COUNT(*) as row_count FROM delivery_events;
" 2>/dev/null || echo "Could not get row counts"

echo ""
echo "Sample Data (Latest Orders):"
PGPASSWORD=$DB_PASSWORD psql -h localhost -p 5432 -U $DB_USER -d $DB_NAME -c "
SELECT 
    o.id as order_id,
    o.customer_id,
    o.status as order_status,
    o.total_amount,
    o.created_at
FROM orders o
ORDER BY o.created_at DESC
LIMIT 5;
" 2>/dev/null || echo "Could not retrieve sample orders"

# =============================================================================
print_section "5. REDIS INSPECTION"
# =============================================================================

echo "Redis Connection Test:"
if docker exec order-processing-redis redis-cli ping > /dev/null 2>&1; then
    print_success "Redis connection successful"
    echo "Redis Info:"
    docker exec order-processing-redis redis-cli info server | grep redis_version || echo "Could not get Redis version"
    
    echo ""
    echo "Redis Key Count:"
    KEY_COUNT=$(docker exec order-processing-redis redis-cli dbsize 2>/dev/null || echo "0")
    echo "Total keys: $KEY_COUNT"
    
    if [ "$KEY_COUNT" != "0" ]; then
        echo ""
        echo "Sample Keys:"
        docker exec order-processing-redis redis-cli keys "*" | head -10 2>/dev/null || echo "Could not list keys"
    fi
else
    print_error "Redis connection failed"
fi

# =============================================================================
print_section "6. SQS/ELASTICMQ INSPECTION"
# =============================================================================

echo "ElasticMQ Connection Test:"
if curl -s http://localhost:9324 > /dev/null 2>&1; then
    print_success "ElasticMQ connection successful"
    
    echo ""
    echo "Queue List:"
    QUEUE_LIST=$(curl -s "http://localhost:9324/?Action=ListQueues&Version=2012-11-05" 2>/dev/null)
    if echo "$QUEUE_LIST" | grep -q "orders-queue.fifo"; then
        print_success "orders-queue.fifo exists"
    else
        print_error "orders-queue.fifo missing"
    fi
    
    if echo "$QUEUE_LIST" | grep -q "delivery-status-queue.fifo"; then
        print_success "delivery-status-queue.fifo exists"
    else
        print_error "delivery-status-queue.fifo missing"
    fi
    
    echo ""
    echo "Raw Queue Response:"
    echo "$QUEUE_LIST"
    
else
    print_error "ElasticMQ connection failed"
fi

# =============================================================================
print_section "7. APPLICATION LOGS"
# =============================================================================

echo "Order Service Logs (last 10 lines):"
if [ -f "logs/order-service.log" ]; then
    tail -10 logs/order-service.log
else
    print_warning "Order Service log file not found"
fi

echo ""
echo "Delivery Service Logs (last 10 lines):"
if [ -f "logs/delivery-service.log" ]; then
    tail -10 logs/delivery-service.log
else
    print_warning "Delivery Service log file not found"
fi

# =============================================================================
print_section "8. SYSTEM RESOURCES"
# =============================================================================

echo "Memory Usage:"
if command -v free > /dev/null 2>&1; then
    free -h
elif command -v vm_stat > /dev/null 2>&1; then
    # macOS
    echo "Memory statistics (macOS):"
    vm_stat | head -5
fi

echo ""
echo "Disk Usage (current directory):"
df -h . 2>/dev/null || echo "Could not get disk usage"

echo ""
echo "Node.js Processes:"
ps aux | grep -E "(node|ts-node)" | grep -v grep || echo "No Node.js processes found"

# =============================================================================
print_section "9. NETWORK CONNECTIVITY"
# =============================================================================

echo "Service Connectivity Tests:"
echo "Order Service API:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}, Time: %{time_total}s\n" http://localhost:3001/health 2>/dev/null || echo "Connection failed"

echo "Delivery Service API:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}, Time: %{time_total}s\n" http://localhost:3002/health 2>/dev/null || echo "Connection failed"

echo "PostgreSQL:"
if PGPASSWORD=$DB_PASSWORD psql -h localhost -p 5432 -U $DB_USER -d $DB_NAME -c "SELECT NOW();" > /dev/null 2>&1; then
    print_success "PostgreSQL connectivity OK"
else
    print_error "PostgreSQL connectivity failed"
fi

# =============================================================================
print_header "🎯 HEALTH CHECK SUMMARY"
# =============================================================================

echo "System Health Report completed at: $(date)"
echo ""
echo "Quick Actions:"
echo "• View live logs: ./scripts/manage-system.sh logs"
echo "• Check status: ./scripts/manage-system.sh status"
echo "• Run demo: ./scripts/manage-system.sh demo"
echo "• Restart system: ./scripts/manage-system.sh restart"
echo ""
print_success "Health check completed!" 