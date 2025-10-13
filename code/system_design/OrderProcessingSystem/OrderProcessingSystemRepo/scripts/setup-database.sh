#!/bin/bash

# Database Setup Script for Order Processing System
# This script creates the required database tables

set -e

echo "🗄️  Setting up Order Processing Database"
echo "========================================"

# Database connection parameters
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-orderprocessing}
DB_USER=${DB_USER:-admin}
DB_PASSWORD=${DB_PASSWORD:-admin123}

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

# Check if PostgreSQL client is available
if ! command -v psql &> /dev/null; then
    print_error "psql (PostgreSQL client) is required but not installed"
    print_warning "Install with: brew install postgresql (macOS) or sudo apt-get install postgresql-client (Ubuntu)"
    exit 1
fi

# Wait for PostgreSQL to be ready
print_step "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1" > /dev/null 2>&1; then
        print_success "PostgreSQL is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "PostgreSQL is not ready after 30 seconds"
        exit 1
    fi
    sleep 1
done

print_success "Database $DB_NAME is ready"

# Create tables
print_step "Creating database tables..."

# Create orders table
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING_SHIPMENT',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on customer_id for faster queries
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
EOF

print_success "Orders table created"

# Create order_items table
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on order_id for faster joins
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
EOF

print_success "Order items table created"

# Create shipments table
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Create shipments table
CREATE TABLE IF NOT EXISTS shipments (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'PROCESSING',
    tracking_number VARCHAR(100),
    carrier VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP WITH TIME ZONE
);

-- Create index on order_id for faster queries
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status);
CREATE INDEX IF NOT EXISTS idx_shipments_tracking_number ON shipments(tracking_number);
EOF

print_success "Shipments table created"

# Create delivery_events table
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Create delivery_events table for audit trail
CREATE TABLE IF NOT EXISTS delivery_events (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_delivery_events_order_id ON delivery_events(order_id);
CREATE INDEX IF NOT EXISTS idx_delivery_events_event_type ON delivery_events(event_type);
CREATE INDEX IF NOT EXISTS idx_delivery_events_created_at ON delivery_events(created_at);

-- Create GIN index for JSONB details column
CREATE INDEX IF NOT EXISTS idx_delivery_events_details ON delivery_events USING GIN (details);
EOF

print_success "Delivery events table created"

# Create a function to update the updated_at timestamp
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
DROP TRIGGER IF EXISTS update_orders_updated_at ON orders;
CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_shipments_updated_at ON shipments;
CREATE TRIGGER update_shipments_updated_at
    BEFORE UPDATE ON shipments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
EOF

print_success "Database triggers created"

# Insert some sample data for testing (optional)
print_step "Inserting sample data..."

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Insert sample data only if tables are empty
INSERT INTO orders (id, customer_id, status, total_amount) 
SELECT 'sample-order-001', 'customer-sample', 'PENDING_SHIPMENT', 99.99
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE id = 'sample-order-001');

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT 'sample-order-001', 'sample-product-001', 1, 99.99
WHERE NOT EXISTS (SELECT 1 FROM order_items WHERE order_id = 'sample-order-001');
EOF

print_success "Sample data inserted"

# Show table information
print_step "Database schema summary:"

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << 'EOF'
-- Show table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    typename,
    char_length,
    description
FROM pg_tables t
LEFT JOIN pg_attribute a ON a.attrelid = t.tablename::regclass
LEFT JOIN pg_type ty ON ty.oid = a.atttypid
LEFT JOIN pg_description d ON d.objoid = a.attrelid AND d.objsubid = a.attnum
WHERE schemaname = 'public' 
    AND tablename IN ('orders', 'order_items', 'shipments', 'delivery_events')
    AND a.attnum > 0
ORDER BY tablename, attnum;
EOF

echo ""
print_success "🎉 Database setup completed successfully!"
echo ""
print_warning "Database connection details:"
echo "• Host: $DB_HOST"
echo "• Port: $DB_PORT"
echo "• Database: $DB_NAME"
echo "• User: $DB_USER"
echo ""
print_warning "Tables created:"
echo "• orders - Main order records"
echo "• order_items - Order line items"
echo "• shipments - Delivery tracking"
echo "• delivery_events - Audit trail"
echo ""
print_warning "To connect manually:"
echo "PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME" 