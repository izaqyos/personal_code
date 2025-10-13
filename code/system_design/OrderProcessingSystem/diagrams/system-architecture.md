# System Architecture Diagram

## High-Level Architecture (Simplified - No API Gateway)

```mermaid
graph TB
    subgraph "External"
        C[Customer/Client]
    end
    
    subgraph "Authentication System"
        AS[Auth Service<br/>:3004<br/>OAuth2 + JWT]
        ADB[(Auth Database<br/>PostgreSQL)]
    end
    
    subgraph "Sales System"
        SA[Sales API Service<br/>:3001<br/>Passport.js]
        SDB[(Sales Database<br/>PostgreSQL)]
    end
    
    subgraph "Delivery System"
        DA[Delivery API Service<br/>:3002]
        DDB[(Delivery Database<br/>PostgreSQL)]
    end
    
    subgraph "Product System"
        PS[Product Service<br/>:3003]
        PDB[(Product Database<br/>PostgreSQL)]
    end
    
    subgraph "Shared Infrastructure"
        MQ[Message Queue<br/>Redis]
    end
    
    subgraph "Observability"
        LOG[Logging]
        MON[Monitoring]
    end
    
    %% Authentication flow
    C -->|1. POST /auth/token<br/>(client credentials)| AS
    AS -->|JWT + Refresh Token| C
    AS -->|Store/Validate Tokens| ADB
    
    %% Authenticated API requests
    C -->|2. POST /api/v1/orders<br/>(Authorization: Bearer JWT)| SA
    SA -->|Passport.js Validation| SA
    SA -->|Order Response| C
    
    %% Internal service communication
    SA -->|HTTP POST /availability| PS
    PS -->|Availability Data| PDB
    
    %% Event-driven communication
    SA -->|Order Created Event| MQ
    MQ -->|Order Event| DA
    DA -->|Status Update Event| MQ
    MQ -->|Status Event| SA
    
    %% Database operations
    SA -->|Store Order| SDB
    DA -->|Store Shipment| DDB
    
    %% Observability
    AS -.->|Logs/Metrics| LOG
    SA -.->|Logs/Metrics| LOG
    DA -.->|Logs/Metrics| LOG
    PS -.->|Logs/Metrics| LOG
    LOG -.->|Aggregate| MON
```

## Architecture Decisions

### Why No API Gateway?
- ✅ **Simple Communication**: Direct service-to-service HTTP calls are sufficient
- ✅ **Reduced Complexity**: Fewer moving parts and potential failure points
- ✅ **Faster Development**: No need to configure and maintain gateway routing
- ✅ **Appropriate Scale**: 3 services don't justify gateway overhead
- ✅ **Cost Effective**: One less component to monitor and maintain

### Service Ports
- **Auth Service**: 3004 (OAuth2 token management)
- **Sales API**: 3001 (Customer-facing, JWT protected)
- **Delivery API**: 3002 (Internal)
- **Product Service**: 3003 (Internal)

### Communication Patterns
1. **OAuth2 Authentication**: Client → Auth Service (token generation/refresh)
2. **JWT Authorization**: Client → Sales API (Passport.js validation)
3. **Synchronous**: Sales ↔ Product (availability check)
4. **Asynchronous**: Sales → Delivery (order events)
5. **Asynchronous**: Delivery → Sales (status updates) 