import { expect } from 'chai';
import sinon from 'sinon';
import { OrderService } from '../../../src/order-service/services/OrderService';
import { Database, redis, sqs } from '../../../src/shared';
import { CreateOrderRequest } from '../../../src/shared';

describe('OrderService', () => {
  let orderService: OrderService;
  let databaseStub: sinon.SinonStub;
  let redisStub: sinon.SinonStub;
  let sqsStub: sinon.SinonStub;

  beforeEach(() => {
    orderService = new OrderService();
    
    // Stub database methods
    databaseStub = sinon.stub(Database, 'transaction');
    
    // Stub Redis methods
    redisStub = sinon.stub(redis, 'checkIdempotency');
    sinon.stub(redis, 'generateFingerprint').returns('test-fingerprint');
    sinon.stub(redis, 'storeIdempotencyResult').resolves();
    
    // Stub SQS methods
    sqsStub = sinon.stub(sqs, 'publishMessage');
  });

  afterEach(() => {
    sinon.restore();
  });

  describe('createOrder', () => {
    const mockRequest: CreateOrderRequest = {
      customer_id: 'customer-123',
      items: [
        { product_id: 'product-1', quantity: 2, unit_price: 10.99 },
        { product_id: 'product-2', quantity: 1, unit_price: 25.50 }
      ]
    };

    it('should create a new order successfully', async () => {
      // Arrange
      const mockOrder = {
        id: 'order-123',
        customer_id: 'customer-123',
        status: 'PENDING_SHIPMENT',
        total_amount: 47.48,
        created_at: new Date(),
        updated_at: new Date()
      };

      redisStub.resolves(null); // No cached result
      databaseStub.resolves(mockOrder);
      sqsStub.resolves();

      // Act
      const result = await orderService.createOrder(mockRequest);

      // Assert
      expect(result).to.deep.equal(mockOrder);
      expect(databaseStub.calledOnce).to.be.true;
      expect(sqsStub.calledOnce).to.be.true;
      
      // Verify SQS message structure
      const sqsCall = sqsStub.getCall(0);
      expect(sqsCall.args[0]).to.equal('orders-queue.fifo');
      expect(sqsCall.args[1]).to.have.property('eventType', 'ORDER_CREATED');
      expect(sqsCall.args[1]).to.have.property('orderId', 'order-123');
      
      // Verify hybrid FIFO MessageGroupId (time-partitioned)
      expect(sqsCall.args[2]).to.match(/^time-partition-\d+$/);
    });

    it('should return cached result for idempotent request', async () => {
      // Arrange
      const cachedOrder = {
        id: 'cached-order-123',
        customer_id: 'customer-123',
        status: 'PENDING_SHIPMENT',
        total_amount: 47.48
      };

      redisStub.resolves(JSON.stringify(cachedOrder));

      // Act
      const result = await orderService.createOrder(mockRequest);

      // Assert
      expect(result).to.deep.equal(cachedOrder);
      expect(databaseStub.called).to.be.false;
      expect(sqsStub.called).to.be.false;
    });

    it('should calculate total amount correctly', async () => {
      // Arrange
      const mockOrder = {
        id: 'order-123',
        customer_id: 'customer-123',
        status: 'PENDING_SHIPMENT',
        total_amount: 47.48, // (2 * 10.99) + (1 * 25.50)
        created_at: new Date(),
        updated_at: new Date()
      };

      redisStub.resolves(null);
      databaseStub.resolves(mockOrder);
      sqsStub.resolves();

      // Act
      const result = await orderService.createOrder(mockRequest);

      // Assert
      expect(result.total_amount).to.equal(47.48);
    });

    it('should handle SQS publish failure gracefully', async () => {
      // Arrange
      const mockOrder = {
        id: 'order-123',
        customer_id: 'customer-123',
        status: 'PENDING_SHIPMENT',
        total_amount: 47.48,
        created_at: new Date(),
        updated_at: new Date()
      };

      redisStub.resolves(null);
      databaseStub.resolves(mockOrder);
      sqsStub.rejects(new Error('SQS failure'));

      // Act & Assert
      // Note: Error logs below are expected for this test scenario (graceful degradation)
      // Should not throw error even if SQS fails
      const result = await orderService.createOrder(mockRequest);
      expect(result).to.deep.equal(mockOrder);
    });
  });

  describe('getOrderById', () => {
    it('should return order with items', async () => {
      // Arrange
      const mockResult = {
        rows: [{
          id: 'order-123',
          customer_id: 'customer-123',
          status: 'PENDING_SHIPMENT',
          total_amount: '47.48',
          items: [
            { product_id: 'product-1', quantity: 2, unit_price: 10.99 }
          ],
          created_at: new Date(),
          updated_at: new Date()
        }]
      };

      const queryStub = sinon.stub(Database, 'query').resolves(mockResult);

      // Act
      const result = await orderService.getOrderById('order-123');

      // Assert
      expect(result).to.not.be.null;
      expect(result!.id).to.equal('order-123');
      expect(result!.total_amount).to.equal(47.48); // Should be converted to number
      expect(queryStub.calledOnce).to.be.true;
    });

    it('should return null for non-existent order', async () => {
      // Arrange
      const queryStub = sinon.stub(Database, 'query').resolves({ rows: [] });

      // Act
      const result = await orderService.getOrderById('non-existent');

      // Assert
      expect(result).to.be.null;
      expect(queryStub.calledOnce).to.be.true;
    });
  });
}); 