# TypeScript Implementation Examples

## Service Interfaces and Types

### Common Types

```typescript
// shared/types/common.ts
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
  items: OrderItem[];
  created_at: Date;
  updated_at: Date;
}

export interface Shipment {
  id: string;
  order_id: string;
  tracking_number?: string;
  carrier?: string;
  status: 'PROCESSING' | 'SHIPPED' | 'IN_TRANSIT' | 'DELIVERED';
  created_at: Date;
  updated_at: Date;
  delivered_at?: Date;
}

export interface Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  available_quantity: number;
  is_active: boolean;
}

export interface Event {
  event_id: string;
  event_type: string;
  timestamp: Date;
  source: string;
  data: any;
}
```

## Sales API Service (TypeScript)

```typescript
// services/sales-api/src/controllers/OrderController.ts
import { Request, Response } from 'express';
import { OrderService } from '../services/OrderService';
import { CreateOrderRequest, OrderResponse } from '../types/order.types';

export class OrderController {
  constructor(private orderService: OrderService) {}

  async createOrder(req: Request<{}, OrderResponse, CreateOrderRequest>, res: Response<OrderResponse>) {
    try {
      // Step 1: Validate input
      const orderRequest = req.body;
      
      // Step 2: Check product availability with Product Service
      const availabilityResult = await this.orderService.checkProductAvailability(orderRequest.items);
      
      if (!availabilityResult.all_available) {
        // Return error immediately if products not available - NO ORDER CREATED
        const unavailableItems = availabilityResult.items.filter(item => !item.is_available);
        return res.status(400).json({
          error: 'PRODUCT_UNAVAILABLE',
          message: 'One or more products are not available',
          details: { unavailable_items: unavailableItems }
        });
      }
      
      // Step 3: Only create order if ALL products available
      const order = await this.orderService.createOrder(orderRequest);
      
      res.status(201).json({
        order_id: order.id,
        status: order.status, // Will be "PENDING_SHIPMENT"
        total_amount: order.total_amount,
        created_at: order.created_at.toISOString()
      });
    } catch (error) {
      res.status(500).json({
        error: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      });
    }
  }

  async getOrder(req: Request<{ order_id: string }>, res: Response) {
    try {
      const order = await this.orderService.getOrderById(req.params.order_id);
      if (!order) {
        return res.status(404).json({ error: 'ORDER_NOT_FOUND' });
      }
      res.json(order);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }

  async updateOrderStatus(req: Request<{ order_id: string }, {}, { status: string }>, res: Response) {
    try {
      const updatedOrder = await this.orderService.updateOrderStatus(
        req.params.order_id,
        req.body.status as Order['status']
      );
      res.json(updatedOrder);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }
}
```

## Sales Service Implementation (TypeScript)

```typescript
// services/sales-api/src/services/OrderService.ts
import { PrismaClient } from '@prisma/client';
import { EventPublisher } from '../utils/EventPublisher';
import { ProductServiceClient } from '../clients/ProductServiceClient';
import { Order, OrderItem } from '../../../shared/types/common';

interface CreateOrderRequest {
  customer_id: string;
  items: OrderItem[];
}

interface AvailabilityResult {
  all_available: boolean;
  items: Array<{
    product_id: string;
    requested: number;
    available: number;
    is_available: boolean;
  }>;
}

export class OrderService {
  constructor(
    private prisma: PrismaClient,
    private eventPublisher: EventPublisher,
    private productClient: ProductServiceClient
  ) {}

  async checkProductAvailability(items: OrderItem[]): Promise<AvailabilityResult> {
    // Call Product Service to check availability
    const availabilityCheck = items.map(item => ({
      product_id: item.product_id,
      quantity: item.quantity
    }));

    return await this.productClient.checkAvailability(availabilityCheck);
  }

  async createOrder(orderRequest: CreateOrderRequest): Promise<Order> {
    // Calculate total amount
    const totalAmount = orderRequest.items.reduce(
      (sum, item) => sum + (item.quantity * item.unit_price), 0
    );

    // Create order in database transaction
    const order = await this.prisma.$transaction(async (tx) => {
      // Create order record
      const newOrder = await tx.order.create({
        data: {
          customer_id: orderRequest.customer_id,
          status: 'PENDING_SHIPMENT', // Set initial status
          total_amount: totalAmount,
          created_at: new Date(),
          updated_at: new Date()
        }
      });

      // Create order items
      await tx.orderItem.createMany({
        data: orderRequest.items.map(item => ({
          order_id: newOrder.id,
          product_id: item.product_id,
          quantity: item.quantity,
          unit_price: item.unit_price
        }))
      });

      return newOrder;
    });

    // Publish order created event AFTER successful order creation
    await this.eventPublisher.publish({
      event_id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      event_type: 'order.created',
      timestamp: new Date(),
      source: 'sales-service',
      data: {
        order_id: order.id,
        customer_id: order.customer_id,
        items: orderRequest.items,
        total_amount: order.total_amount
      }
    });

    return order;
  }

  async getOrderById(orderId: string): Promise<Order | null> {
    return this.prisma.order.findUnique({
      where: { id: orderId },
      include: { order_items: true }
    });
  }

  async updateOrderStatus(orderId: string, status: Order['status']): Promise<Order> {
    return this.prisma.order.update({
      where: { id: orderId },
      data: {
        status,
        updated_at: new Date()
      }
    });
  }
}

// services/sales-api/src/clients/ProductServiceClient.ts
import axios, { AxiosInstance } from 'axios';

interface AvailabilityCheckItem {
  product_id: string;
  quantity: number;
}

export class ProductServiceClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.PRODUCT_SERVICE_URL || 'http://product-service:3000') {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'X-Service-Name': 'sales-api' // For internal service identification
      }
    });
  }

  async checkAvailability(items: AvailabilityCheckItem[]): Promise<AvailabilityResult> {
    try {
      const response = await this.client.post('/api/v1/products/check-availability', {
        items
      });
      return response.data;
    } catch (error) {
      console.error('Product Service availability check failed:', error);
      // Fail safe: assume products are unavailable if service is down
      throw new Error('Product Service unavailable');
    }
  }
}
```

## Delivery API Service (TypeScript)

```typescript
// services/delivery-api/src/controllers/DeliveryController.ts
import { Request, Response } from 'express';
import { DeliveryService } from '../services/DeliveryService';
import { CreateShipmentRequest, UpdateShipmentStatusRequest } from '../types/delivery.types';

export class DeliveryController {
  constructor(private deliveryService: DeliveryService) {}

  async createShipment(req: Request<{}, {}, CreateShipmentRequest>, res: Response) {
    try {
      const shipment = await this.deliveryService.createShipment(req.body);
      res.status(201).json(shipment);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }

  async updateShipmentStatus(req: Request<{ shipment_id: string }, {}, UpdateShipmentStatusRequest>, res: Response) {
    try {
      const shipment = await this.deliveryService.updateShipmentStatus(
        req.params.shipment_id,
        req.body.status,
        req.body.tracking_number
      );
      res.json(shipment);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }

  async getShipment(req: Request<{ shipment_id: string }>, res: Response) {
    try {
      const shipment = await this.deliveryService.getShipmentById(req.params.shipment_id);
      if (!shipment) {
        return res.status(404).json({ error: 'SHIPMENT_NOT_FOUND' });
      }
      res.json(shipment);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }
}

// services/delivery-api/src/services/DeliveryService.ts
import { PrismaClient } from '@prisma/client';
import { EventPublisher } from '../utils/EventPublisher';
import { Shipment } from '../../../shared/types/common';

export class DeliveryService {
  constructor(
    private prisma: PrismaClient,
    private eventPublisher: EventPublisher
  ) {}

  async createShipment(orderData: { order_id: string; customer_id: string }): Promise<Shipment> {
    const shipment = await this.prisma.shipment.create({
      data: {
        order_id: orderData.order_id,
        status: 'PROCESSING',
        created_at: new Date(),
        updated_at: new Date()
      }
    });

    // Publish shipment created event
    await this.eventPublisher.publish({
      event_id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      event_type: 'shipment.created',
      timestamp: new Date(),
      source: 'delivery-service',
      data: { shipment_id: shipment.id, order_id: orderData.order_id }
    });

    return shipment;
  }

  async updateShipmentStatus(
    shipmentId: string,
    status: Shipment['status'],
    trackingNumber?: string
  ): Promise<Shipment> {
    const shipment = await this.prisma.shipment.update({
      where: { id: shipmentId },
      data: {
        status,
        tracking_number: trackingNumber,
        updated_at: new Date(),
        delivered_at: status === 'DELIVERED' ? new Date() : undefined
      }
    });

    // Publish status update event
    await this.eventPublisher.publish({
      event_id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      event_type: 'order.status_updated',
      timestamp: new Date(),
      source: 'delivery-service',
      data: {
        order_id: shipment.order_id,
        previous_status: 'PENDING_SHIPMENT', // This should be fetched from previous state
        current_status: this.mapDeliveryStatusToOrderStatus(status),
        tracking_number: trackingNumber
      }
    });

    return shipment;
  }

  private mapDeliveryStatusToOrderStatus(deliveryStatus: Shipment['status']): Order['status'] {
    switch (deliveryStatus) {
      case 'PROCESSING':
        return 'PENDING_SHIPMENT';
      case 'SHIPPED':
      case 'IN_TRANSIT':
        return 'SHIPPED';
      case 'DELIVERED':
        return 'DELIVERED';
      default:
        return 'PENDING_SHIPMENT';
    }
  }

  async getShipmentById(shipmentId: string): Promise<Shipment | null> {
    return this.prisma.shipment.findUnique({
      where: { id: shipmentId }
    });
  }
}
```

## Product Service (TypeScript)

```typescript
// services/product-service/src/controllers/ProductController.ts
import { Request, Response } from 'express';
import { ProductService } from '../services/ProductService';
import { CheckAvailabilityRequest } from '../types/product.types';

export class ProductController {
  constructor(private productService: ProductService) {}

  async getProductAvailability(req: Request<{ product_id: string }>, res: Response) {
    try {
      const availability = await this.productService.getProductAvailability(req.params.product_id);
      if (!availability) {
        return res.status(404).json({ error: 'PRODUCT_NOT_FOUND' });
      }
      res.json(availability);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }

  async checkAvailability(req: Request<{}, {}, CheckAvailabilityRequest>, res: Response) {
    try {
      const result = await this.productService.checkAvailability(req.body.items);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: 'INTERNAL_ERROR' });
    }
  }
}

// services/product-service/src/services/ProductService.ts
import { PrismaClient } from '@prisma/client';
import { Product, OrderItem } from '../../../shared/types/common';

interface AvailabilityCheck {
  product_id: string;
  requested: number;
  available: number;
  is_available: boolean;
}

interface AvailabilityResult {
  all_available: boolean;
  items: AvailabilityCheck[];
}

export class ProductService {
  constructor(private prisma: PrismaClient) {}

  async getProductAvailability(productId: string) {
    const product = await this.prisma.product.findUnique({
      where: { id: productId, is_active: true }
    });

    if (!product) return null;

    return {
      product_id: product.id,
      available_quantity: product.available_quantity,
      is_available: product.available_quantity > 0,
      last_updated: product.updated_at.toISOString()
    };
  }

  async checkAvailability(items: Array<{ product_id: string; quantity: number }>): Promise<AvailabilityResult> {
    const productIds = items.map(item => item.product_id);
    const products = await this.prisma.product.findMany({
      where: { id: { in: productIds }, is_active: true }
    });

    const productMap = new Map(products.map(p => [p.id, p]));
    
    const checks: AvailabilityCheck[] = items.map(item => {
      const product = productMap.get(item.product_id);
      const available = product?.available_quantity || 0;
      
      return {
        product_id: item.product_id,
        requested: item.quantity,
        available,
        is_available: available >= item.quantity
      };
    });

    return {
      all_available: checks.every(check => check.is_available),
      items: checks
    };
  }

  async updateProductQuantity(productId: string, quantityChange: number): Promise<Product | null> {
    try {
      return await this.prisma.product.update({
        where: { id: productId },
        data: {
          available_quantity: {
            increment: quantityChange
          },
          updated_at: new Date()
        }
      });
    } catch (error) {
      return null;
    }
  }
}
```

## Message Queue Event Publisher (TypeScript)

```typescript
// shared/utils/EventPublisher.ts
import Redis from 'ioredis';
import { Event } from '../types/common';

export class EventPublisher {
  constructor(private redis: Redis) {}

  async publish(event: Event): Promise<void> {
    try {
      const eventData = JSON.stringify(event);
      await this.redis.xadd('events', '*', 'data', eventData);
      console.log(`Event published: ${event.event_type}`, { event_id: event.event_id });
    } catch (error) {
      console.error('Failed to publish event:', error);
      throw error;
    }
  }
}

// shared/utils/EventSubscriber.ts
export class EventSubscriber {
  constructor(private redis: Redis, private consumerGroup: string) {}

  async subscribe(eventType: string, handler: (event: Event) => Promise<void>): Promise<void> {
    try {
      // Ensure consumer group exists
      await this.redis.xgroup('CREATE', 'events', this.consumerGroup, '$', 'MKSTREAM');
    } catch (error) {
      // Group might already exist
    }

    while (true) {
      try {
        const messages = await this.redis.xreadgroup(
          'GROUP', this.consumerGroup, 'consumer1',
          'COUNT', 10,
          'BLOCK', 1000,
          'STREAMS', 'events', '>'
        );

        if (messages && messages.length > 0) {
          for (const [stream, streamMessages] of messages) {
            for (const [messageId, fields] of streamMessages) {
              try {
                const eventData = JSON.parse(fields[1]); // fields[1] is the 'data' field
                const event: Event = {
                  event_id: eventData.event_id,
                  event_type: eventData.event_type,
                  timestamp: new Date(eventData.timestamp),
                  source: eventData.source,
                  data: eventData.data
                };

                if (event.event_type === eventType) {
                  await handler(event);
                }

                // Acknowledge message
                await this.redis.xack('events', this.consumerGroup, messageId);
              } catch (error) {
                console.error('Failed to process message:', error);
              }
            }
          }
        }
      } catch (error) {
        console.error('Error in event subscriber:', error);
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  }
}
```

## Docker Configuration for TypeScript Services

```dockerfile
# Dockerfile.typescript (template for all services)
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/

# Build TypeScript
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy package files and install production dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy built application
COPY --from=builder /app/dist ./dist

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Run the application
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

All services will be implemented in TypeScript with consistent patterns, type safety, and shared type definitions for better maintainability and development experience.

## OAuth2 Authentication Flow Example

### Client Authentication Request
```typescript
// Example client request to Auth Service
const authRequest = {
  grant_type: 'client_credentials',
  client_id: 'sales_client_123',
  client_secret: 'secure_client_secret_456',
  scope: 'orders:create orders:read'
};

const response = await fetch('http://auth-service:3004/auth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(authRequest)
});

const tokens = await response.json();
// tokens = { access_token: "jwt...", refresh_token: "refresh...", expires_in: 3600 }
```

### Sales API Request with JWT
```typescript
// Client making authenticated request to Sales API
const orderRequest = {
  customer_id: "customer_123",
  items: [
    { product_id: "product_456", quantity: 2, unit_price: 29.99 }
  ]
};

const response = await fetch('http://sales-api:3001/api/v1/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${tokens.access_token}`
  },
  body: JSON.stringify(orderRequest)
});
```

### Protected Sales API Controller (Updated)
```typescript
// services/sales-api/src/controllers/OrderController.ts
export class OrderController {
  async createOrder(req: AuthenticatedRequest, res: Response) {
    try {
      // req.user is populated by Passport.js middleware
      const clientId = req.user.clientId;
      const scopes = req.user.scopes;
      
      // Check if client has required scope
      if (!scopes.includes('orders:create')) {
        return res.status(403).json({
          error: 'insufficient_scope',
          message: 'Missing required scope: orders:create'
        });
      }
      
      // Log the authenticated request
      console.log(`Order creation request from client: ${clientId}`);
      
      // Proceed with order creation logic...
      const orderRequest = req.body;
      const availabilityResult = await this.orderService.checkProductAvailability(orderRequest.items);
      
      if (!availabilityResult.all_available) {
        const unavailableItems = availabilityResult.items.filter(item => !item.is_available);
        return res.status(400).json({
          error: 'PRODUCT_UNAVAILABLE',
          message: 'One or more products are not available',
          details: { unavailable_items: unavailableItems }
        });
      }
      
      const order = await this.orderService.createOrder(orderRequest);
      
      res.status(201).json({
        order_id: order.id,
        status: order.status,
        total_amount: order.total_amount,
        created_at: order.created_at.toISOString()
      });
    } catch (error) {
      res.status(500).json({
        error: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      });
    }
  }
}

interface AuthenticatedRequest extends Request {
  user: {
    clientId: string;
    scopes: string[];
    rateLimit: {
      requests_per_minute: number;
    };
  };
}
``` 