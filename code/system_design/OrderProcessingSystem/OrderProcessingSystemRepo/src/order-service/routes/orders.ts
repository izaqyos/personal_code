import { Router, Request, Response } from 'express';
// @ts-ignore
import { authenticateJWT, AuthenticatedRequest } from '../middleware/auth';
import { OrderService } from '../services/OrderService';
import { CreateOrderRequest, OrderResponse } from '../../shared';
import { logger } from '../../shared';

const router = Router();
const orderService = new OrderService();

// Apply JWT authentication to all order routes
router.use(authenticateJWT as any);

// Create new order
router.post('/', async (req: any, res: Response) => {
  try {
    const orderRequest: CreateOrderRequest = req.body;
    
    // Basic validation for PoC
    // Production would have comprehensive validation (Joi, class-validator, etc.)
    if (!orderRequest.customer_id || !orderRequest.items || orderRequest.items.length === 0) {
      return res.status(400).json({
        error: 'VALIDATION_ERROR',
        message: 'Missing required fields: customer_id, items',
      });
    }

    // Validate items
    for (const item of orderRequest.items) {
      if (!item.product_id || !item.quantity || !item.unit_price || 
          item.quantity <= 0 || item.unit_price <= 0) {
        return res.status(400).json({
          error: 'VALIDATION_ERROR',
          message: 'Invalid item data: product_id, quantity > 0, unit_price > 0 required',
        });
      }
    }

    const order = await orderService.createOrder(orderRequest);
    
    const response: OrderResponse = {
      order_id: order.id,
      status: order.status,
      total_amount: order.total_amount,
      created_at: order.created_at.toISOString(),
    };

    logger.info('Order created successfully', { 
      orderId: order.id, 
      customerId: order.customer_id,
      totalAmount: order.total_amount 
    });

    res.status(201).json(response);
  } catch (error) {
    logger.error('Order creation failed', { 
      error: error instanceof Error ? error.message : error,
      body: req.body 
    });

    if (error instanceof Error && error.message.includes('PRODUCT_UNAVAILABLE')) {
      return res.status(400).json({
        error: 'PRODUCT_UNAVAILABLE',
        message: 'One or more products are not available',
      });
    }

    res.status(500).json({
      error: 'INTERNAL_ERROR',
      message: 'Failed to create order',
    });
  }
});

// Get order by ID
router.get('/:orderId', async (req: any, res: Response) => {
  try {
    const { orderId } = req.params;
    
    if (!orderId) {
      return res.status(400).json({
        error: 'VALIDATION_ERROR',
        message: 'Order ID is required',
      });
    }

    const order = await orderService.getOrderById(orderId);
    
    if (!order) {
      return res.status(404).json({
        error: 'ORDER_NOT_FOUND',
        message: 'Order not found',
      });
    }

    logger.info('Order retrieved', { orderId });
    res.json(order);
  } catch (error) {
    logger.error('Order retrieval failed', { 
      error: error instanceof Error ? error.message : error,
      orderId: req.params.orderId 
    });

    res.status(500).json({
      error: 'INTERNAL_ERROR',
      message: 'Failed to retrieve order',
    });
  }
});

export { router as orderRoutes }; 