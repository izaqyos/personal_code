import { Router, Request, Response } from 'express';
import { DeliveryService } from '../services/DeliveryService';
import { logger } from '../../shared';

const router = Router();
const deliveryService = new DeliveryService();

// Get shipment by order ID
router.get('/shipment/:orderId', async (req: Request, res: Response) => {
  try {
    const { orderId } = req.params;
    
    if (!orderId) {
      return res.status(400).json({
        error: 'VALIDATION_ERROR',
        message: 'Order ID is required',
      });
    }

    const shipment = await deliveryService.getShipmentByOrderId(orderId);
    
    if (!shipment) {
      return res.status(404).json({
        error: 'SHIPMENT_NOT_FOUND',
        message: 'Shipment not found for this order',
      });
    }

    logger.info('Shipment retrieved', { orderId, shipmentId: shipment.id });
    res.json(shipment);
  } catch (error) {
    logger.error('Shipment retrieval failed', { 
      error: error instanceof Error ? error.message : error,
      orderId: req.params.orderId 
    });

    res.status(500).json({
      error: 'INTERNAL_ERROR',
      message: 'Failed to retrieve shipment',
    });
  }
});

// Simulate delivery status update (for demo purposes)
router.post('/shipment/:shipmentId/status', async (req: Request, res: Response) => {
  try {
    const { shipmentId } = req.params;
    const { status } = req.body;
    
    if (!shipmentId || !status) {
      return res.status(400).json({
        error: 'VALIDATION_ERROR',
        message: 'Shipment ID and status are required',
      });
    }

    const validStatuses = ['PROCESSING', 'SHIPPED', 'DELIVERED'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({
        error: 'VALIDATION_ERROR',
        message: `Status must be one of: ${validStatuses.join(', ')}`,
      });
    }

    const updatedShipment = await deliveryService.updateShipmentStatus(
      shipmentId, 
      status,
      req.body.tracking_number,
      req.body.carrier
    );

    if (!updatedShipment) {
      return res.status(404).json({
        error: 'SHIPMENT_NOT_FOUND',
        message: 'Shipment not found',
      });
    }

    logger.info('Shipment status updated', { 
      shipmentId, 
      status, 
      orderId: updatedShipment.order_id 
    });

    res.json(updatedShipment);
  } catch (error) {
    logger.error('Shipment status update failed', { 
      error: error instanceof Error ? error.message : error,
      shipmentId: req.params.shipmentId 
    });

    res.status(500).json({
      error: 'INTERNAL_ERROR',
      message: 'Failed to update shipment status',
    });
  }
});

export { router as deliveryRoutes }; 