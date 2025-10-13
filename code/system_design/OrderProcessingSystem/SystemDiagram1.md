graph TB
    subgraph "External"
        C[Customer]
        EXT[External Systems]
    end
    
    subgraph "API Gateway Layer"
        AG[API Gateway]
    end
    
    subgraph "Sales System"
        SA[Sales API Service]
        SDB[(Sales Database<br/>PostgreSQL)]
    end
    
    subgraph "Delivery System"
        DA[Delivery API Service]
        DDB[(Delivery Database<br/>PostgreSQL)]
    end
    
    subgraph "Shared Infrastructure"
        MQ[Message Queue<br/>Redis/RabbitMQ]
        PM[Product Service]
        PDB[(Product Database<br/>PostgreSQL)]
    end
    
    subgraph "Observability"
        LOG[Logging Service]
        MON[Monitoring]
        TRACE[Tracing]
    end
    
    %% Customer interactions
    C -->|Place Order| AG
    AG -->|Route Request| SA
    SA -->|Order Response| C
    
    %% Order flow
    SA -->|Check Availability| PM
    PM -->|Product Data| PDB
    SA -->|Store Order| SDB
    SA -->|Order Created Event| MQ
    MQ -->|Process Order| DA
    DA -->|Store Delivery| DDB
    
    %% Status updates
    DA -->|Status Update Event| MQ
    MQ -->|Update Status| SA
    SA -->|Update Order| SDB
    
    %% External integrations
    DA -->|Delivery Updates| EXT
    
    %% Observability
    SA -.->|Logs/Metrics| LOG
    DA -.->|Logs/Metrics| LOG
    PM -.->|Logs/Metrics| LOG
    LOG -.->|Aggregate| MON
    SA -.->|Traces| TRACE
    DA -.->|Traces| TRACE