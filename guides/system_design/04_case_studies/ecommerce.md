# E-Commerce Platform Design

Design an e-commerce platform like Amazon or Shopify.

## Requirements

### Functional Requirements
- Product catalog (browse, search, filter)
- Shopping cart
- Checkout and payment processing
- Order management
- Inventory management
- User accounts and authentication
- Reviews and ratings
- Seller management (marketplace)

### Non-Functional Requirements
- High availability (99.99%)
- Low latency (< 200ms for browsing)
- Handle flash sales (100x traffic spike)
- Data consistency for inventory and payments
- Scale: 10M daily users, 1M orders/day

## Capacity Estimation

### Traffic
```
DAU: 10M users
Page views: 100M/day = 1,150/second
Peak: 10,000/second (flash sales)

Orders: 1M/day = 11.5 orders/second
Peak: 1,000 orders/second
```

### Storage
```
Products: 10M × 10KB = 100 GB
Orders: 1M/day × 5KB = 5 GB/day = 1.8 TB/year
Users: 50M × 2KB = 100 GB
Images: 10M products × 5 images × 500KB = 25 TB
```

## High-Level Design

```
                         ┌──────────────┐
                         │     CDN      │
                         └──────┬───────┘
                                │
                         ┌──────┴───────┐
                         │ API Gateway  │
                         └──────┬───────┘
                                │
    ┌───────────────────────────┼───────────────────────────┐
    │                           │                           │
    ▼                           ▼                           ▼
┌─────────┐              ┌─────────────┐              ┌─────────┐
│ Product │              │   Order     │              │  User   │
│ Service │              │  Service    │              │ Service │
└────┬────┘              └──────┬──────┘              └────┬────┘
     │                          │                          │
┌────┴────┐              ┌──────┴──────┐              ┌────┴────┐
│Product  │              │ Order DB    │              │ User DB │
│ DB      │              │             │              │         │
└─────────┘              └─────────────┘              └─────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
             ┌──────────────┐       ┌──────────────┐
             │   Payment    │       │  Inventory   │
             │   Service    │       │   Service    │
             └──────────────┘       └──────────────┘
```

## Product Catalog

### Product Service Architecture

```
           ┌──────────────────────────────┐
           │       Product Service        │
           └──────────────┬───────────────┘
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼
┌──────────┐      ┌──────────────┐      ┌──────────┐
│ Search   │      │   Primary    │      │  Cache   │
│(Elastic) │      │   Database   │      │ (Redis)  │
└──────────┘      └──────────────┘      └──────────┘
```

### Product Schema

```sql
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    seller_id UUID,
    name VARCHAR(200),
    description TEXT,
    category_id UUID,
    price DECIMAL(10, 2),
    currency VARCHAR(3),
    status VARCHAR(20),  -- 'active', 'inactive', 'deleted'
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE product_variants (
    variant_id UUID PRIMARY KEY,
    product_id UUID REFERENCES products,
    sku VARCHAR(50) UNIQUE,
    attributes JSONB,  -- {"size": "M", "color": "blue"}
    price_delta DECIMAL(10, 2) DEFAULT 0,
    image_urls TEXT[]
);
```

### Search with Elasticsearch

```json
{
  "mappings": {
    "properties": {
      "name": { "type": "text", "analyzer": "standard" },
      "description": { "type": "text" },
      "category": { "type": "keyword" },
      "price": { "type": "float" },
      "attributes": { "type": "nested" },
      "rating": { "type": "float" },
      "seller_id": { "type": "keyword" }
    }
  }
}
```

```python
def search_products(query, filters, page=1, size=20):
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": query,
                        "fields": ["name^3", "description"]
                    }}
                ],
                "filter": []
            }
        },
        "sort": [{"_score": "desc"}, {"rating": "desc"}],
        "from": (page - 1) * size,
        "size": size
    }
    
    if filters.get("category"):
        body["query"]["bool"]["filter"].append(
            {"term": {"category": filters["category"]}}
        )
    
    if filters.get("price_range"):
        body["query"]["bool"]["filter"].append(
            {"range": {"price": {
                "gte": filters["price_range"][0],
                "lte": filters["price_range"][1]
            }}}
        )
    
    return es.search(index="products", body=body)
```

## Shopping Cart

### Cart Design Options

**Option 1: Database-backed (persistent)**
```sql
CREATE TABLE cart_items (
    cart_id UUID,
    user_id UUID,
    product_id UUID,
    variant_id UUID,
    quantity INT,
    added_at TIMESTAMP,
    PRIMARY KEY (cart_id, product_id, variant_id)
);
```

**Option 2: Redis-backed (session-based)**
```python
class CartService:
    def add_item(self, user_id, product_id, quantity):
        cart_key = f"cart:{user_id}"
        
        # Hash: product_id → quantity
        self.redis.hincrby(cart_key, product_id, quantity)
        
        # Set expiry for abandoned carts
        self.redis.expire(cart_key, 7 * 24 * 3600)  # 7 days
    
    def get_cart(self, user_id):
        cart_key = f"cart:{user_id}"
        items = self.redis.hgetall(cart_key)
        
        # Fetch product details
        product_ids = list(items.keys())
        products = product_service.get_products(product_ids)
        
        return [
            {
                "product": products[pid],
                "quantity": int(qty)
            }
            for pid, qty in items.items()
        ]
```

### Cart Merge (Guest → Logged In)

```python
def merge_carts(guest_id, user_id):
    guest_cart = get_cart(guest_id)
    user_cart = get_cart(user_id)
    
    for item in guest_cart:
        existing = find_item(user_cart, item.product_id)
        if existing:
            existing.quantity += item.quantity
        else:
            user_cart.append(item)
    
    save_cart(user_id, user_cart)
    delete_cart(guest_id)
```

## Inventory Management

### Inventory Schema

```sql
CREATE TABLE inventory (
    sku VARCHAR(50) PRIMARY KEY,
    warehouse_id UUID,
    quantity INT,
    reserved INT DEFAULT 0,
    version INT DEFAULT 0,  -- Optimistic locking
    updated_at TIMESTAMP
);

CREATE INDEX idx_warehouse ON inventory(warehouse_id);
```

### Inventory Operations

```python
class InventoryService:
    def reserve_stock(self, sku, quantity):
        """Reserve stock for checkout"""
        with db.transaction():
            inventory = db.query(
                "SELECT * FROM inventory WHERE sku = ? FOR UPDATE",
                sku
            )
            
            available = inventory.quantity - inventory.reserved
            
            if available < quantity:
                raise InsufficientStock(sku, available, quantity)
            
            db.execute(
                "UPDATE inventory SET reserved = reserved + ? WHERE sku = ?",
                quantity, sku
            )
            
            return ReservationToken(sku, quantity, expires_in=15*60)
    
    def commit_reservation(self, reservation_token):
        """Finalize purchase"""
        with db.transaction():
            db.execute("""
                UPDATE inventory 
                SET quantity = quantity - ?,
                    reserved = reserved - ?
                WHERE sku = ?
            """, reservation_token.quantity, 
                 reservation_token.quantity,
                 reservation_token.sku)
    
    def release_reservation(self, reservation_token):
        """Cancel reservation"""
        db.execute(
            "UPDATE inventory SET reserved = reserved - ? WHERE sku = ?",
            reservation_token.quantity, reservation_token.sku
        )
```

### Flash Sale Handling

```python
class FlashSaleInventory:
    def __init__(self):
        self.redis = Redis()
    
    def setup_flash_sale(self, product_id, quantity):
        # Pre-load inventory to Redis
        self.redis.set(f"flash:{product_id}:stock", quantity)
    
    def try_purchase(self, product_id, user_id, quantity=1):
        # Atomic decrement with Lua script
        script = """
        local stock = tonumber(redis.call('get', KEYS[1]))
        if stock >= tonumber(ARGV[1]) then
            redis.call('decrby', KEYS[1], ARGV[1])
            return 1
        else
            return 0
        end
        """
        
        success = self.redis.eval(
            script, 
            keys=[f"flash:{product_id}:stock"],
            args=[quantity]
        )
        
        if success:
            # Queue actual order processing
            queue.publish("flash_orders", {
                "product_id": product_id,
                "user_id": user_id,
                "quantity": quantity
            })
            return True
        return False
```

## Order Processing

### Order Flow

```
Cart → Checkout → Payment → Order Created → Fulfillment
                     │
              ┌──────┴──────┐
              ▼             ▼
         Success        Failure
              │             │
              ▼             ▼
        Confirm         Rollback
        Inventory       Reservation
```

### Order Saga

```python
class OrderSaga:
    def execute(self, order_request):
        try:
            # Step 1: Reserve inventory
            reservations = inventory_service.reserve_all(
                order_request.items
            )
            
            # Step 2: Process payment
            payment = payment_service.charge(
                order_request.user_id,
                order_request.total,
                order_request.payment_method
            )
            
            # Step 3: Create order
            order = order_service.create(
                order_request,
                payment.transaction_id
            )
            
            # Step 4: Commit inventory
            inventory_service.commit_all(reservations)
            
            # Step 5: Notify fulfillment
            fulfillment_queue.publish(order)
            
            return order
            
        except PaymentError as e:
            # Rollback inventory
            inventory_service.release_all(reservations)
            raise
            
        except Exception as e:
            # Rollback everything
            if payment:
                payment_service.refund(payment.transaction_id)
            if reservations:
                inventory_service.release_all(reservations)
            raise
```

### Order Schema

```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID,
    status VARCHAR(20),  -- 'pending', 'paid', 'shipped', 'delivered'
    total DECIMAL(10, 2),
    currency VARCHAR(3),
    shipping_address JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE order_items (
    order_id UUID REFERENCES orders,
    product_id UUID,
    variant_id UUID,
    quantity INT,
    unit_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id, variant_id)
);
```

## Payment Processing

### Payment Flow

```
Client → Order Service → Payment Service → Payment Gateway
                              │
                        ┌─────┴─────┐
                        ▼           ▼
                    Stripe       PayPal
```

### Idempotency

```python
class PaymentService:
    def charge(self, idempotency_key, amount, payment_method):
        # Check if already processed
        existing = db.query(
            "SELECT * FROM payments WHERE idempotency_key = ?",
            idempotency_key
        )
        
        if existing:
            return existing  # Return cached result
        
        # Process payment
        result = stripe.charges.create(
            amount=amount,
            currency="usd",
            source=payment_method,
            idempotency_key=idempotency_key
        )
        
        # Store result
        db.execute("""
            INSERT INTO payments (idempotency_key, result, created_at)
            VALUES (?, ?, NOW())
        """, idempotency_key, result)
        
        return result
```

## Caching Strategy

### Multi-Layer Caching

```
Browser Cache (static assets)
    │
CDN Cache (product images, static pages)
    │
API Cache (Redis - product data, user sessions)
    │
Database Query Cache (frequently accessed data)
```

### Cache Invalidation

```python
def update_product(product_id, data):
    # Update database
    db.update("products", product_id, data)
    
    # Invalidate caches
    cache.delete(f"product:{product_id}")
    cache.delete(f"product_page:{product_id}")
    
    # Update search index
    search_index.update("products", product_id, data)
    
    # Notify CDN
    cdn.purge(f"/products/{product_id}*")
```

## Scaling Considerations

### Database Sharding

```
Products: Shard by category
Orders: Shard by user_id
Inventory: Shard by warehouse_id
```

### Read Replicas

```
                 ┌─────────────┐
                 │   Primary   │ ← Writes
                 └──────┬──────┘
           ┌───────────┼───────────┐
           ▼           ▼           ▼
      ┌─────────┐ ┌─────────┐ ┌─────────┐
      │ Replica │ │ Replica │ │ Replica │ ← Reads
      └─────────┘ └─────────┘ └─────────┘
```

### Microservices Boundaries

```
Product Service ─── Product DB + Elasticsearch
Order Service ───── Order DB
Payment Service ─── Payment DB + Gateway integration
Inventory Service ─ Inventory DB
User Service ────── User DB
```

## Trade-offs

| Decision | Trade-off |
|----------|-----------|
| SQL vs NoSQL | Consistency vs scale |
| Cart in Redis vs DB | Speed vs persistence |
| Sync vs async payment | UX vs reliability |
| Strong vs eventual consistency | Accuracy vs availability |

## Interview Tips

1. Start with core flows (browse, cart, checkout)
2. Detail inventory management (concurrency)
3. Explain order saga for distributed transactions
4. Discuss payment idempotency
5. Address flash sale scenarios
6. Consider caching at multiple layers

## Related Topics

- [Saga Pattern](../03_design_patterns/saga_pattern.md)
- [Databases](../02_building_blocks/databases.md)
- [Caching](../02_building_blocks/caching.md)
