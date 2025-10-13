sequenceDiagram
    participant C as Customer
    participant AG as API Gateway
    participant SA as Sales API
    participant PS as Product Service
    participant DB as Sales DB
    participant MQ as Message Queue
    participant DA as Delivery API
    participant DDB as Delivery DB
    
    Note over C,DDB: Order Creation Flow
    
    C->>AG: POST /orders (order request)
    AG->>SA: Forward order request
    
    SA->>SA: Validate order data
    SA->>PS: Check product availability
    PS-->>SA: Product availability response
    
    alt Product Available
        SA->>DB: Create order record
        SA->>DB: Set status "PENDING_SHIPMENT"
        SA->>MQ: Publish "order.created" event
        SA-->>C: Return order ID & status
        
        Note over MQ,DDB: Async Delivery Processing
        
        MQ->>DA: Consume "order.created" event
        DA->>DDB: Create shipment record
        DA->>DDB: Set status "PROCESSING"
        
        Note over DA,DDB: Shipment Processing
        
        DA->>DA: Process shipment
        DA->>DDB: Update status "SHIPPED"
        DA->>MQ: Publish "order.status_updated" event
        
        MQ->>SA: Consume status update event
        SA->>DB: Update order status "SHIPPED"
        
        Note over DA,DDB: Delivery Completion
        
        DA->>DA: Mark as delivered
        DA->>DDB: Update status "DELIVERED"
        DA->>MQ: Publish "order.status_updated" event
        
        MQ->>SA: Consume status update event
        SA->>DB: Update order status "DELIVERED"
        
    else Product Unavailable
        SA-->>C: Return error (Product unavailable)
    end