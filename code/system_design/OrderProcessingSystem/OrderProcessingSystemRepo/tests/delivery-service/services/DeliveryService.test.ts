import { expect } from 'chai';
import sinon from 'sinon';
import { DeliveryService } from '../../../src/delivery-service/services/DeliveryService';
import { Database, sqs } from '../../../src/shared';
import { OrderCreatedEvent } from '../../../src/shared';

describe('DeliveryService', () => {
  let deliveryService: DeliveryService;
  let databaseStub: sinon.SinonStub;
  let sqsStub: sinon.SinonStub;

  beforeEach(() => {
    deliveryService = new DeliveryService();
    
    // Stub database methods
    databaseStub = sinon.stub(Database, 'query');
    
    // Stub SQS methods
    sqsStub = sinon.stub(sqs, 'publishMessage');
  });

  afterEach(() => {
    sinon.restore();
  });

  describe('processOrderCreated', () => {
    const mockEvent: OrderCreatedEvent = {
      eventType: 'ORDER_CREATED',
      orderId: 'order-123',
      customerId: 'customer-123',
      items: [
        { product_id: 'product-1', quantity: 2, unit_price: 10.99 }
      ],
      totalAmount: 21.98,
      timestamp: new Date()
    };

    it('should create shipment for new order', async () => {
      // Arrange
      databaseStub.resolves({ rows: [] });

      // Act
      await deliveryService.processOrderCreated(mockEvent);

      // Assert
      expect(databaseStub.calledTwice).to.be.true;
      
      // First call should create shipment
      const firstCall = databaseStub.getCall(0);
      expect(firstCall.args[0]).to.include('INSERT INTO shipments');
      expect(firstCall.args[1]).to.include('order-123');
      expect(firstCall.args[1]).to.include('PROCESSING');
      
      // Second call should log delivery event
      const secondCall = databaseStub.getCall(1);
      expect(secondCall.args[0]).to.include('INSERT INTO delivery_events');
    });

    it('should handle database errors gracefully', async () => {
      // Arrange
      databaseStub.rejects(new Error('Database error'));

      // Act & Assert
      // Note: Error logs below are expected for this test scenario
      try {
        await deliveryService.processOrderCreated(mockEvent);
        expect.fail('Should have thrown error');
      } catch (error) {
        expect(error).to.be.instanceOf(Error);
        expect((error as Error).message).to.equal('Database error');
      }
    });
  });

  describe('getShipmentByOrderId', () => {
    it('should return shipment for valid order ID', async () => {
      // Arrange
      const mockShipment = {
        id: 'shipment-123',
        order_id: 'order-123',
        status: 'PROCESSING',
        created_at: new Date(),
        updated_at: new Date()
      };

      databaseStub.resolves({ rows: [mockShipment] });

      // Act
      const result = await deliveryService.getShipmentByOrderId('order-123');

      // Assert
      expect(result).to.deep.equal(mockShipment);
      expect(databaseStub.calledOnce).to.be.true;
      expect(databaseStub.getCall(0).args[0]).to.include('SELECT * FROM shipments');
      expect(databaseStub.getCall(0).args[1]).to.deep.equal(['order-123']);
    });

    it('should return null for non-existent order', async () => {
      // Arrange
      databaseStub.resolves({ rows: [] });

      // Act
      const result = await deliveryService.getShipmentByOrderId('non-existent');

      // Assert
      expect(result).to.be.null;
      expect(databaseStub.calledOnce).to.be.true;
    });
  });

  describe('updateShipmentStatus', () => {
    it('should update shipment status and order status', async () => {
      // Arrange
      const mockShipment = {
        id: 'shipment-123',
        order_id: 'order-123',
        status: 'SHIPPED',
        tracking_number: 'TRK123456',
        carrier: 'Demo Carrier',
        created_at: new Date(),
        updated_at: new Date()
      };

      const mockOrder = {
        status: 'PENDING_SHIPMENT'
      };

      // Mock database calls
      databaseStub.onCall(0).resolves({ rows: [mockShipment] }); // Update shipment
      databaseStub.onCall(1).resolves({ rows: [] }); // Log delivery event
      databaseStub.onCall(2).resolves({ rows: [mockOrder] }); // Get order status
      databaseStub.onCall(3).resolves({ rows: [] }); // Update order status

      sqsStub.resolves();

      // Act
      const result = await deliveryService.updateShipmentStatus(
        'shipment-123',
        'SHIPPED',
        'TRK123456',
        'Demo Carrier'
      );

      // Assert
      expect(result).to.deep.equal(mockShipment);
      expect(databaseStub.callCount).to.equal(4);
      expect(sqsStub.calledOnce).to.be.true;
      
      // Verify SQS event for status update
      const sqsCall = sqsStub.getCall(0);
      expect(sqsCall.args[0]).to.equal('order-updates-queue.fifo');
      expect(sqsCall.args[1]).to.have.property('eventType', 'ORDER_STATUS_UPDATE');
      expect(sqsCall.args[1]).to.have.property('orderId', 'order-123');
      expect(sqsCall.args[1]).to.have.property('currentStatus', 'SHIPPED');
      
      // Verify hybrid FIFO MessageGroupId for status updates (time-partitioned)
      expect(sqsCall.args[2]).to.match(/^time-partition-\d+$/);
    });

    it('should return null for non-existent shipment', async () => {
      // Arrange
      databaseStub.resolves({ rows: [] });

      // Act
      const result = await deliveryService.updateShipmentStatus(
        'non-existent',
        'SHIPPED'
      );

      // Assert
      expect(result).to.be.null;
      expect(databaseStub.calledOnce).to.be.true;
    });

    it('should handle delivered status with timestamp', async () => {
      // Arrange
      const mockShipment = {
        id: 'shipment-123',
        order_id: 'order-123',
        status: 'DELIVERED',
        delivered_at: new Date(),
        created_at: new Date(),
        updated_at: new Date()
      };

      const mockOrder = { status: 'SHIPPED' };

      databaseStub.onCall(0).resolves({ rows: [mockShipment] });
      databaseStub.onCall(1).resolves({ rows: [] });
      databaseStub.onCall(2).resolves({ rows: [mockOrder] });
      databaseStub.onCall(3).resolves({ rows: [] });

      sqsStub.resolves();

      // Act
      const result = await deliveryService.updateShipmentStatus(
        'shipment-123',
        'DELIVERED'
      );

      // Assert
      expect(result).to.deep.equal(mockShipment);
      
      // Verify delivered_at is set in the update query
      const updateCall = databaseStub.getCall(0);
      expect(updateCall.args[0]).to.include('delivered_at = $4');
    });
  });
}); 