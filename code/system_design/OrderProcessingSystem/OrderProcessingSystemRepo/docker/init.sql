-- Initialize Order Processing System Database

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('PENDING_SHIPMENT', 'SHIPPED', 'DELIVERED')),
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create shipments table
-- NOTE: For KISS principle, product_id and customer_id are kept as strings
-- without FK constraints to products/customers tables (mocked for PoC)
CREATE TABLE IF NOT EXISTS shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL UNIQUE REFERENCES orders(id) ON DELETE CASCADE,
    tracking_number VARCHAR(255) UNIQUE,
    carrier VARCHAR(100),
    status VARCHAR(50) NOT NULL CHECK (status IN ('PROCESSING', 'SHIPPED', 'DELIVERED')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    delivered_at TIMESTAMP WITH TIME ZONE
);

-- Create delivery_events table for audit trail
-- NOTE: This table will grow unbounded without TTL. For production, consider:
-- 1. PostgreSQL partitioning with auto-drop (pg_partman extension)
-- 2. Application-level cleanup job (DELETE events older than X days)
-- 3. Archive strategy (move old events to separate archive table)
-- For PoC simplicity, we will not handle TTL for now.
CREATE TABLE IF NOT EXISTS delivery_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_id UUID NOT NULL REFERENCES shipments(id),
    event_type VARCHAR(50) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status);
CREATE INDEX IF NOT EXISTS idx_delivery_events_shipment_id ON delivery_events(shipment_id);

-- Insert some sample data for testing
INSERT INTO orders (id, customer_id, status, total_amount) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'customer_123', 'PENDING_SHIPMENT', 59.98)
ON CONFLICT (id) DO NOTHING;

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'product_456', 2, 29.99)
ON CONFLICT (id) DO NOTHING; 