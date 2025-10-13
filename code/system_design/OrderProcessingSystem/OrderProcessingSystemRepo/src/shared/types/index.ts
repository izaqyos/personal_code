// Shared types for Order Processing System
// Note: Keeping simple for PoC. Production would have more validation and complex types.

export interface OrderItem {
  product_id: string;
  quantity: number;
  unit_price: number;
}

export interface Order {
  id: string;
  customer_id: string;
  status: 'PENDING_SHIPMENT' | 'SHIPPED' | 'DELIVERED';
  total_amount: number;
  items?: OrderItem[];
  created_at: Date;
  updated_at: Date;
}

export interface Shipment {
  id: string;
  order_id: string;
  tracking_number?: string;
  carrier?: string;
  status: 'PROCESSING' | 'SHIPPED' | 'DELIVERED';
  created_at: Date;
  updated_at: Date;
  delivered_at?: Date;
}

export interface CreateOrderRequest {
  customer_id: string;
  items: OrderItem[];
}

export interface OrderResponse {
  order_id: string;
  status: string;
  total_amount: number;
  created_at: string;
}

// SQS Event types
export interface OrderCreatedEvent {
  eventType: 'ORDER_CREATED';
  orderId: string;
  customerId: string;
  items: OrderItem[];
  totalAmount: number;
  timestamp: Date;
}

export interface OrderStatusUpdateEvent {
  eventType: 'ORDER_STATUS_UPDATE';
  orderId: string;
  previousStatus: Order['status'];
  currentStatus: Order['status'];
  timestamp: Date;
  trackingNumber?: string;
  carrier?: string;
}

// Auth types
export interface JWTPayload {
  clientId: string;
  iat: number;
  exp: number;
}

// API Response types
export interface ApiError {
  error: string;
  message: string;
  details?: any;
} 