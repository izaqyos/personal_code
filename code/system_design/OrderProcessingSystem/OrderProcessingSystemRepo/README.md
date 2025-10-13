# Order Processing System PoC

A microservices-based order processing system with SQS FIFO queues, JWT auth, and polling-based status updates (*real-time notifications planned*).

## 📚 Documentation

- 📋 **[System Design Document](SYSTEM_DESIGN.md)** - Complete architecture and design decisions
- 🚀 **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Detailed implementation guide and features
- 🎮 **[Demo Guide](DEMO_GUIDE.md)** - Complete demo walkthrough with expected outputs
- 📖 **[API Examples](demo/curl-examples.md)** - Manual API testing instructions
- 🗺️ **[Documentation Map](DOCUMENTATION_MAP.md)** - How all docs connect together

## Architecture

- **Order Service**: Auth + order creation + polling API for status
- **Delivery Service**: Shipment processing + status updates  
- **Infrastructure**: PostgreSQL + Redis + SQS FIFO with **hybrid 30s time-partitioned ordering** (~600 TPS)
- **Status Updates**: Currently polling-based (*real-time WebSocket/SSE planned*)

> 🏗️ **Design Philosophy**: This 2-service architecture follows KISS principles, prioritizing simplicity and low operational costs. See [System Design](SYSTEM_DESIGN.md) for detailed rationale.

## 🚀 Quick Start

### Option 1: Unified Management (Recommended)
```bash
# Start everything (infrastructure + services)
./scripts/manage-system.sh up

# Check system health
./scripts/health-check.sh

# Run interactive demo
./scripts/manage-system.sh demo

# Check system status
./scripts/manage-system.sh status

# View logs
./scripts/manage-system.sh logs

# Stop everything
./scripts/manage-system.sh down
```

### Option 2: Legacy Scripts
```bash
# One-command setup - starts everything
./scripts/start-services.sh

# Run interactive demo
./demo/demo.sh
```

### Option 3: Manual Development Setup
```bash
# 1. Setup infrastructure
npm run docker:up
cp env.example .env

# 2. Install dependencies
npm install

# 3. Setup database
./scripts/setup-database.sh

# 4. Run services in development mode
npm run dev:order    # Order service on :3001
npm run dev:delivery # Delivery service on :3002
```

## 🛠️ System Management

### Start the System
```bash
# Start all services (infrastructure + applications)
./scripts/manage-system.sh up

# Expected output:
# ✓ Environment setup
# ✓ Dependencies installed
# ✓ Infrastructure services started (PostgreSQL, Redis, ElasticMQ)
# ✓ Database setup completed
# ✓ SQS queues created
# ✓ Order Service started (PID: xxxx)
# ✓ Delivery Service started (PID: xxxx)
# ✓ Health checks passed
```

### Check System Health
```bash
# Comprehensive health inspection
./scripts/health-check.sh

# Provides detailed status for:
# - Docker infrastructure (PostgreSQL, Redis, ElasticMQ)
# - Port usage inspection
# - Application services status
# - Database connectivity and data
# - Redis inspection
# - SQS/ElasticMQ queues
# - Application logs
# - System resources
# - Network connectivity
```

### Monitor System Status
```bash
# Quick status check
./scripts/manage-system.sh status

# Shows:
# - Application Services: Running/Stopped with PIDs
# - Health checks: ✓ Healthy / ✗ Unhealthy
# - Infrastructure Services: PostgreSQL, Redis, ElasticMQ status
```

### View System Logs
```bash
# Follow all logs in real-time
./scripts/manage-system.sh logs

# Shows logs from:
# - Docker services (PostgreSQL, Redis, ElasticMQ)
# - Order Service application logs
# - Delivery Service application logs
```

### Stop the System
```bash
# Stop all services and clean up
./scripts/manage-system.sh down

# Stops:
# - Order Service (graceful shutdown)
# - Delivery Service (graceful shutdown)
# - Docker infrastructure services
# - Removes PID files
```

### Restart the System
```bash
# Restart all services
./scripts/manage-system.sh restart

# Equivalent to: down → sleep 2s → up
```

## 🎮 Running the Demo

### Interactive Demo
```bash
# Start the comprehensive demo
./scripts/manage-system.sh demo

# The demo will:
# 1. Create a new order with sample products
# 2. Process the order through delivery service
# 3. Track status updates in real-time
# 4. Show complete order lifecycle
# 5. Validate all system components
```

### Manual Demo Steps
```bash
# 1. Ensure system is running
./scripts/manage-system.sh up
./scripts/health-check.sh

# 2. Create test order
curl -X POST http://localhost:3001/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(node -e "console.log(require('jsonwebtoken').sign({userId: 'demo-user'}, 'dev-secret-key-change-in-production'))")" \
  -d '{
    "customerId": "demo-customer-001",
    "items": [
      {"productId": "laptop-001", "quantity": 1, "unitPrice": 999.99}
    ]
  }'

# 3. Check order status (polling - no real-time notifications yet)
curl -X GET http://localhost:3001/api/orders/{ORDER_ID} \
  -H "Authorization: Bearer {JWT_TOKEN}"

# 4. Monitor logs
./scripts/manage-system.sh logs
```

> 📖 **See [Demo Guide](DEMO_GUIDE.md)** for complete demo walkthrough with expected outputs and troubleshooting.

## 🔧 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check what's using the ports
./scripts/health-check.sh  # Section 2: Port Usage Inspection

# Kill processes using required ports
sudo lsof -ti:3001 | xargs kill -9  # Order Service port
sudo lsof -ti:3002 | xargs kill -9  # Delivery Service port
```

**Database connection issues:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Check database connectivity
./scripts/health-check.sh  # Section 4: Database Inspection

# Restart database
docker-compose restart postgres
```

**SQS queue issues:**
```bash
# Check ElasticMQ status
curl -s "http://localhost:9324/?Action=ListQueues&Version=2012-11-05"

# Recreate queues
curl -X POST "http://localhost:9324/?Action=CreateQueue&QueueName=orders-queue.fifo&Attribute.1.Name=FifoQueue&Attribute.1.Value=true"
```

**Service health check failures:**
```bash
# Check individual service health
curl http://localhost:3001/health | jq .
curl http://localhost:3002/health | jq .

# Check logs for errors
./scripts/manage-system.sh logs
```

### Testing
```bash
# Run unit tests
npm test

# Run linting
npm run lint

# Run integration demo
./scripts/manage-system.sh demo
```

> 💡 **See [Implementation Summary](IMPLEMENTATION_SUMMARY.md)** for detailed setup instructions and troubleshooting.

## API Endpoints

### Auth
- `POST /auth/token` - Get JWT token

### Orders
- `POST /orders` - Create order (requires JWT)
- `GET /orders/:id` - Get order status

### Health
- `GET /health` - Service health check

## Queue Management

- **ElasticMQ UI**: http://localhost:9325
- **Queues**: `orders-queue.fifo`, `delivery-status-queue.fifo`

## Tech Stack

- **Runtime**: Node.js + TypeScript
- **Framework**: Express + Passport.js
- **Database**: PostgreSQL
- **Cache**: Redis  
- **Queues**: SQS FIFO (ElasticMQ for local dev)
- **Testing**: Mocha + Sinon + Chai
- **Linting**: ESLint + TypeScript

> 🔧 **Technology Rationale**: Each choice optimizes for the specific requirements. See [System Design](SYSTEM_DESIGN.md) for detailed technology decisions and [Implementation Summary](IMPLEMENTATION_SUMMARY.md) for feature implementation details.

## 📁 Project Structure

```
OrderProcessingSystemRepo/
├── src/
│   ├── shared/                 # Shared utilities and types
│   ├── order-service/         # Order API service
│   └── delivery-service/      # Delivery worker service
├── tests/                     # Unit tests (mirrors src/ structure)
│   ├── order-service/        # Order Service tests
│   └── delivery-service/     # Delivery Service tests
├── demo/                      # Demo scripts and examples
├── scripts/                   # Setup and utility scripts
│   ├── manage-system.sh       # Unified system management
│   ├── health-check.sh        # Comprehensive health inspection
│   ├── setup-database.sh      # Database initialization
│   └── start-services.sh      # Legacy startup script
├── docker-compose.yml         # Infrastructure setup
├── README.md                  # This file
├── DEMO_GUIDE.md             # Complete demo walkthrough
├── SYSTEM_DESIGN.md          # Architecture documentation
└── IMPLEMENTATION_SUMMARY.md  # Implementation details
```

> 📖 **See [Implementation Summary](IMPLEMENTATION_SUMMARY.md)** for detailed code organization and architecture patterns.

---

## 📚 Next Steps

- **🏗️ Architecture**: Read the [System Design Document](SYSTEM_DESIGN.md) for complete architectural decisions
- **🚀 Implementation**: Check the [Implementation Summary](IMPLEMENTATION_SUMMARY.md) for detailed features and setup
- **🎯 Demo**: Run `./scripts/manage-system.sh demo` for a complete end-to-end demonstration
- **📖 Demo Guide**: See [Demo Guide](DEMO_GUIDE.md) for detailed demo walkthrough with expected outputs
- **📖 API Testing**: See [curl examples](demo/curl-examples.md) for manual API testing

## 🎯 Management Commands Quick Reference

| Command | Description |
|---------|-------------|
| `./scripts/manage-system.sh up` | Start all services |
| `./scripts/manage-system.sh down` | Stop all services |
| `./scripts/manage-system.sh restart` | Restart all services |
| `./scripts/manage-system.sh status` | Check service status |
| `./scripts/manage-system.sh logs` | View all logs |
| `./scripts/manage-system.sh demo` | Run interactive demo |
| `./scripts/health-check.sh` | Comprehensive health check |
| `npm test` | Run unit tests |
