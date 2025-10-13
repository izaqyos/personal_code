# System Design Diagrams

This directory contains all the architectural and sequence diagrams for the E-Commerce Order Processing Integration system.

## 📊 Diagram Files

### **Updated Diagrams** (Latest Design)
- **[system-architecture.md](./system-architecture.md)** - High-level system architecture (No API Gateway)
- **[order-creation-sequence.md](./order-creation-sequence.md)** - Complete order creation flow with availability check

### **Legacy Diagrams** (Existing)
- **SystemDiagram1.md** - Previous system diagram
- **SequenceDiagram1.md** - Previous sequence diagram  
- **SystemSeqDiagram1.png** - Previous sequence diagram (PNG)
- **SystemHLDiagram1.png** - Previous high-level diagram (PNG)

## 🎯 Key Design Decisions Reflected

### 1. **No API Gateway Architecture**
The system architecture diagram shows direct customer interaction with the Sales API, removing unnecessary complexity for a 3-service system.

### 2. **Product Availability Check Flow**
The sequence diagram demonstrates the critical requirement where:
- Product Service validates availability **BEFORE** order creation
- Order ID and "PENDING_SHIPMENT" status are set **ONLY** if products are available
- No order creation occurs if products are unavailable

### 3. **Service Communication Patterns**
- **Synchronous**: Sales ↔ Product (availability check)
- **Asynchronous**: Sales → Delivery (order events)
- **Asynchronous**: Delivery → Sales (status updates)

## 🔧 Technology Stack
- **All Services**: TypeScript + Node.js + Express.js + Prisma
- **Databases**: PostgreSQL (separate per service)
- **Message Queue**: Redis with Redis Streams
- **Containerization**: Docker + Docker Compose

## 📋 Service Ports
- **Sales API**: 3001 (Customer-facing)
- **Delivery API**: 3002 (Internal)
- **Product Service**: 3003 (Internal)

## 🚀 Usage

### View Diagrams
The `.md` files contain Mermaid diagrams that can be rendered in:
- GitHub/GitLab (automatic rendering)
- VS Code (with Mermaid extension)
- Mermaid Live Editor
- Most markdown viewers

### Modify Diagrams
1. Edit the Mermaid code in the respective `.md` files
2. Use [Mermaid Live Editor](https://mermaid.live/) for real-time preview
3. Export as PNG/SVG if needed for documentation

## 📖 Related Documentation
- **[System_Design_Plan.md](../System_Design_Plan.md)** - Complete system design document
- **[TypeScript_Implementation_Examples.md](../TypeScript_Implementation_Examples.md)** - Implementation examples
- **[Product Requirements Document.pdf](../Product%20Requirements%20Document.pdf)** - Original requirements 