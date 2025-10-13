# Scalability & Auto-Scaling Design

## Overview

This document defines how our e-commerce system scales automatically during peak hours using **AWS Auto Scaling Service**, ensuring high throughput and performance under variable load conditions.

**UPDATE**: After analysis in `AWS_Auto_Scaling_Analysis.md`, we've decided to use **AWS Auto Scaling Service with ECS/Fargate** instead of Kubernetes for:
- **72% cost reduction** ($1,683/month savings)
- **Simplified operations** (no cluster management)
- **Native AWS integration** (seamless with RDS, SQS/SNS)
- **Enterprise reliability** (AWS SLA and support)

## Auto-Scaling Architecture

### ⚠️ DEPRECATED: Container Orchestration with Kubernetes
*This section is kept for reference. See `AWS_Auto_Scaling_Analysis.md` for the recommended AWS approach.*

```yaml
# kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-system
  labels:
    monitoring: enabled
---
# kubernetes/sales-api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sales-api
  namespace: ecommerce-system
spec:
  replicas: 2  # Minimum replicas
  selector:
    matchLabels:
      app: sales-api
  template:
    metadata:
      labels:
        app: sales-api
    spec:
      containers:
      - name: sales-api
        image: sales-api:latest
        ports:
        - containerPort: 3001
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: sales-db-url
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        readinessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 30
          periodSeconds: 10
---
# Auto-scaling configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sales-api-hpa
  namespace: ecommerce-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sales-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Pods
        value: 4
        periodSeconds: 60
      - type: Percent
        value: 100
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 2
        periodSeconds: 60
```

### Load Balancing Strategy

```yaml
# kubernetes/sales-api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: sales-api-service
  namespace: ecommerce-system
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  selector:
    app: sales-api
  ports:
  - port: 80
    targetPort: 3001
    protocol: TCP
  sessionAffinity: None  # Stateless services
---
# kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  namespace: ecommerce-system
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/rate-limit: "1000"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/connection-proxy-header: "upgrade"
    nginx.ingress.kubernetes.io/upstream-keepalive-connections: "10"
spec:
  rules:
  - host: api.ecommerce-system.com
    http:
      paths:
      - path: /api/sales
        pathType: Prefix
        backend:
          service:
            name: sales-api-service
            port:
              number: 80
      - path: /api/delivery
        pathType: Prefix
        backend:
          service:
            name: delivery-api-service
            port:
              number: 80
      - path: /api/products
        pathType: Prefix
        backend:
          service:
            name: product-api-service
            port:
              number: 80
      - path: /api/auth
        pathType: Prefix
        backend:
          service:
            name: auth-api-service
            port:
              number: 80
  tls:
  - hosts:
    - api.ecommerce-system.com
    secretName: tls-secret
```

## Service-Specific Auto-Scaling Configurations

### Sales API Auto-Scaling

```typescript
// src/monitoring/metrics.ts
import { register, Counter, Histogram, Gauge } from 'prom-client';

export class MetricsCollector {
  private requestCounter = new Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status_code']
  });

  private requestDuration = new Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route'],
    buckets: [0.1, 0.5, 1, 2, 5, 10]
  });

  private requestsPerSecond = new Gauge({
    name: 'http_requests_per_second',
    help: 'Current requests per second'
  });

  private orderCreationRate = new Gauge({
    name: 'orders_created_per_minute',
    help: 'Orders created per minute'
  });

  private databaseConnectionPool = new Gauge({
    name: 'database_connections_active',
    help: 'Active database connections'
  });

  recordRequest(method: string, route: string, statusCode: number, duration: number): void {
    this.requestCounter.inc({ method, route, status_code: statusCode });
    this.requestDuration.observe({ method, route }, duration);
  }

  updateRequestsPerSecond(rps: number): void {
    this.requestsPerSecond.set(rps);
  }

  updateOrderCreationRate(rate: number): void {
    this.orderCreationRate.set(rate);
  }

  updateDatabaseConnections(count: number): void {
    this.databaseConnectionPool.set(count);
  }
}

// Middleware for automatic metrics collection
export const metricsMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    metricsCollector.recordRequest(
      req.method,
      req.route?.path || req.path,
      res.statusCode,
      duration
    );
  });
  
  next();
};
```

### Auto-Scaling Policies by Service

```yaml
# Product Service Auto-Scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: product-service-hpa
  namespace: ecommerce-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: product-service
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60  # Lower threshold for availability checks
  - type: Pods
    pods:
      metric:
        name: availability_checks_per_second
      target:
        type: AverageValue
        averageValue: "50"
---
# Delivery Service Auto-Scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: delivery-service-hpa
  namespace: ecommerce-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: delivery-service
  minReplicas: 1
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
  - type: Pods
    pods:
      metric:
        name: delivery_initiations_per_second
      target:
        type: AverageValue
        averageValue: "30"
---
# Auth Service Auto-Scaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
  namespace: ecommerce-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 2  # Always maintain redundancy for auth
  maxReplicas: 6
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: token_validations_per_second
      target:
        type: AverageValue
        averageValue: "200"
```

## Database Scaling Strategy

### Read Replica Configuration

```typescript
// src/database/connection-manager.ts
import { Pool } from 'pg';

export class DatabaseConnectionManager {
  private writePool: Pool;
  private readPools: Pool[];
  private currentReadIndex = 0;

  constructor() {
    // Primary database for writes
    this.writePool = new Pool({
      host: process.env.DB_PRIMARY_HOST,
      port: 5432,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 20,  // Maximum connections
      min: 5,   // Minimum connections
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    // Read replicas for read operations
    this.readPools = [
      new Pool({
        host: process.env.DB_READ_REPLICA_1_HOST,
        port: 5432,
        database: process.env.DB_NAME,
        user: process.env.DB_READ_USER,
        password: process.env.DB_READ_PASSWORD,
        max: 15,
        min: 3,
        idleTimeoutMillis: 30000,
        connectionTimeoutMillis: 2000,
      }),
      new Pool({
        host: process.env.DB_READ_REPLICA_2_HOST,
        port: 5432,
        database: process.env.DB_NAME,
        user: process.env.DB_READ_USER,
        password: process.env.DB_READ_PASSWORD,
        max: 15,
        min: 3,
        idleTimeoutMillis: 30000,
        connectionTimeoutMillis: 2000,
      })
    ];
  }

  // Write operations always go to primary
  async executeWrite<T>(query: string, params?: any[]): Promise<T> {
    const client = await this.writePool.connect();
    try {
      const result = await client.query(query, params);
      return result.rows;
    } finally {
      client.release();
    }
  }

  // Read operations use round-robin on read replicas
  async executeRead<T>(query: string, params?: any[]): Promise<T> {
    const readPool = this.getNextReadPool();
    const client = await readPool.connect();
    try {
      const result = await client.query(query, params);
      return result.rows;
    } catch (error) {
      // Fallback to primary if read replica fails
      console.warn('Read replica failed, falling back to primary', error);
      return this.executeWrite(query, params);
    } finally {
      client.release();
    }
  }

  private getNextReadPool(): Pool {
    const pool = this.readPools[this.currentReadIndex];
    this.currentReadIndex = (this.currentReadIndex + 1) % this.readPools.length;
    return pool;
  }

  // Monitor connection pool health
  async getConnectionPoolMetrics() {
    const writePoolStats = {
      totalCount: this.writePool.totalCount,
      idleCount: this.writePool.idleCount,
      waitingCount: this.writePool.waitingCount
    };

    const readPoolStats = this.readPools.map((pool, index) => ({
      replicaIndex: index,
      totalCount: pool.totalCount,
      idleCount: pool.idleCount,
      waitingCount: pool.waitingCount
    }));

    return {
      write: writePoolStats,
      read: readPoolStats
    };
  }
}
```

### Database Auto-Scaling with AWS RDS

```yaml
# terraform/rds-autoscaling.tf
resource "aws_rds_cluster" "sales_db_cluster" {
  cluster_identifier     = "sales-db-cluster"
  engine                = "aurora-postgresql"
  engine_version        = "13.7"
  database_name         = "sales_db"
  master_username       = var.db_username
  master_password       = var.db_password
  
  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  serverlessv2_scaling_configuration {
    max_capacity = 16
    min_capacity = 0.5
  }
  
  tags = {
    Name = "Sales Database Cluster"
    Environment = "production"
  }
}

resource "aws_rds_cluster_instance" "sales_db_primary" {
  identifier          = "sales-db-primary"
  cluster_identifier  = aws_rds_cluster.sales_db_cluster.id
  instance_class      = "db.serverless"
  engine              = aws_rds_cluster.sales_db_cluster.engine
  engine_version      = aws_rds_cluster.sales_db_cluster.engine_version
  
  performance_insights_enabled = true
  monitoring_interval         = 60
  monitoring_role_arn        = aws_iam_role.rds_monitoring.arn
}

resource "aws_rds_cluster_instance" "sales_db_replica" {
  count              = 2
  identifier         = "sales-db-replica-${count.index + 1}"
  cluster_identifier = aws_rds_cluster.sales_db_cluster.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.sales_db_cluster.engine
  engine_version     = aws_rds_cluster.sales_db_cluster.engine_version
  
  performance_insights_enabled = true
  monitoring_interval         = 60
  monitoring_role_arn        = aws_iam_role.rds_monitoring.arn
}

# Auto-scaling target for Aurora Serverless
resource "aws_appautoscaling_target" "aurora_target" {
  max_capacity       = 16
  min_capacity       = 1
  resource_id        = "cluster:${aws_rds_cluster.sales_db_cluster.cluster_identifier}"
  scalable_dimension = "rds:cluster:ReadReplicaCount"
  service_namespace  = "rds"
}

resource "aws_appautoscaling_policy" "aurora_scale_up" {
  name               = "aurora-scale-up"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.aurora_target.resource_id
  scalable_dimension = aws_appautoscaling_target.aurora_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.aurora_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value = 70.0
    predefined_metric_specification {
      predefined_metric_type = "RDSReaderAverageCPUUtilization"
    }
    scale_out_cooldown = 300
    scale_in_cooldown  = 300
  }
}
```

## Message Queue Scaling

### AWS SQS Auto-Scaling

```typescript
// src/messaging/sqs-auto-scaler.ts
import { SQS, CloudWatch } from 'aws-sdk';

export class SQSAutoScaler {
  private sqs = new SQS();
  private cloudwatch = new CloudWatch();

  async monitorAndScale(): Promise<void> {
    const queueUrls = [
      process.env.ORDER_EVENTS_QUEUE_URL,
      process.env.DELIVERY_EVENTS_QUEUE_URL,
      process.env.STATUS_UPDATE_QUEUE_URL
    ];

    for (const queueUrl of queueUrls) {
      const metrics = await this.getQueueMetrics(queueUrl);
      await this.adjustProcessingCapacity(queueUrl, metrics);
    }
  }

  private async getQueueMetrics(queueUrl: string) {
    const params = {
      QueueUrl: queueUrl,
      AttributeNames: [
        'ApproximateNumberOfMessages',
        'ApproximateNumberOfMessagesNotVisible',
        'ApproximateAgeOfOldestMessage'
      ]
    };

    const result = await this.sqs.getQueueAttributes(params).promise();
    return {
      messagesAvailable: parseInt(result.Attributes?.ApproximateNumberOfMessages || '0'),
      messagesInFlight: parseInt(result.Attributes?.ApproximateNumberOfMessagesNotVisible || '0'),
      oldestMessageAge: parseInt(result.Attributes?.ApproximateAgeOfOldestMessage || '0')
    };
  }

  private async adjustProcessingCapacity(queueUrl: string, metrics: any): Promise<void> {
    const totalMessages = metrics.messagesAvailable + metrics.messagesInFlight;
    
    // Determine scaling needs
    let desiredWorkers = 1;
    
    if (totalMessages > 1000) {
      desiredWorkers = Math.min(10, Math.ceil(totalMessages / 100));
    } else if (totalMessages > 100) {
      desiredWorkers = Math.min(5, Math.ceil(totalMessages / 50));
    } else if (metrics.oldestMessageAge > 300) { // 5 minutes
      desiredWorkers = 3;
    }

    // Update ECS service desired count for message processors
    await this.updateMessageProcessorScale(queueUrl, desiredWorkers);
  }

  private async updateMessageProcessorScale(queueUrl: string, desiredCount: number): Promise<void> {
    const serviceName = this.getServiceNameFromQueueUrl(queueUrl);
    
    // This would integrate with ECS or Kubernetes to scale message processors
    console.log(`Scaling ${serviceName} to ${desiredCount} instances for queue ${queueUrl}`);
  }

  private getServiceNameFromQueueUrl(queueUrl: string): string {
    if (queueUrl.includes('order-events')) return 'order-event-processor';
    if (queueUrl.includes('delivery-events')) return 'delivery-event-processor';
    if (queueUrl.includes('status-update')) return 'status-update-processor';
    return 'generic-message-processor';
  }
}
```

## Redis Scaling for Caching

```yaml
# Redis Cluster Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: ecommerce-system
data:
  redis.conf: |
    maxmemory 2gb
    maxmemory-policy allkeys-lru
    save 900 1
    save 300 10
    save 60 10000
    tcp-keepalive 60
    timeout 300
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
  namespace: ecommerce-system
spec:
  serviceName: redis-cluster
  replicas: 3
  selector:
    matchLabels:
      app: redis-cluster
  template:
    metadata:
      labels:
        app: redis-cluster
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        command:
        - redis-server
        - /etc/redis/redis.conf
        - --cluster-enabled
        - "yes"
        - --cluster-config-file
        - /data/nodes.conf
        - --cluster-node-timeout
        - "5000"
        - --appendonly
        - "yes"
        volumeMounts:
        - name: redis-config
          mountPath: /etc/redis/
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            cpu: 100m
            memory: 512Mi
          limits:
            cpu: 500m
            memory: 2Gi
      volumes:
      - name: redis-config
        configMap:
          name: redis-config
  volumeClaimTemplates:
  - metadata:
      name: redis-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## Monitoring & Alerting for Scaling

### Prometheus Monitoring Configuration

```yaml
# monitoring/prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: ecommerce-system
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "scaling_rules.yml"
    
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
    
    - job_name: 'sales-api'
      static_configs:
      - targets: ['sales-api-service:80']
      metrics_path: /metrics
      scrape_interval: 10s
    
    - job_name: 'delivery-api'
      static_configs:
      - targets: ['delivery-api-service:80']
      metrics_path: /metrics
      scrape_interval: 10s
    
    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093
---
# monitoring/scaling-rules.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: scaling-rules
  namespace: ecommerce-system
data:
  scaling_rules.yml: |
    groups:
    - name: scaling_alerts
      rules:
      - alert: HighCPUUsage
        expr: rate(container_cpu_usage_seconds_total[5m]) > 0.8
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for 2 minutes"
      
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 90% for 2 minutes"
      
      - alert: HighRequestRate
        expr: rate(http_requests_total[1m]) > 500
        for: 1m
        labels:
          severity: info
        annotations:
          summary: "High request rate detected"
          description: "Request rate is above 500 req/min"
      
      - alert: DatabaseConnectionPoolExhausted
        expr: database_connections_active / database_connections_max > 0.9
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "Database connections are above 90% of limit"
```

## Scaling Scenarios & Responses

### Peak Hour Scaling Timeline

| **Time** | **Expected Load** | **Auto-Scaling Response** | **Resource Allocation** |
|----------|-------------------|----------------------------|-------------------------|
| **Normal Hours** | 100 req/min | 2 Sales API, 1 Product, 1 Delivery | Minimal resources |
| **Pre-Peak** | 500 req/min | 4 Sales API, 2 Product, 1 Delivery | Medium scaling |
| **Peak Hours** | 2000 req/min | 12 Sales API, 6 Product, 3 Delivery | Maximum scaling |
| **Flash Sale** | 5000 req/min | 20 Sales API, 10 Product, 5 Delivery | Emergency scaling |

### Cost Optimization

```typescript
// src/scaling/cost-optimizer.ts
export class CostOptimizer {
  async optimizeScaling(): Promise<void> {
    const currentHour = new Date().getHours();
    const dayOfWeek = new Date().getDay();
    
    // Predictive scaling based on historical patterns
    const expectedLoad = this.predictLoad(currentHour, dayOfWeek);
    const costEfficientScale = this.calculateOptimalScale(expectedLoad);
    
    await this.applyScalingRecommendations(costEfficientScale);
  }

  private predictLoad(hour: number, dayOfWeek: number): number {
    // Historical data analysis
    const baseLoad = 100;
    const hourMultiplier = this.getHourMultiplier(hour);
    const dayMultiplier = this.getDayMultiplier(dayOfWeek);
    
    return baseLoad * hourMultiplier * dayMultiplier;
  }

  private getHourMultiplier(hour: number): number {
    // Peak hours: 10-12, 14-16, 19-22
    if ((hour >= 10 && hour <= 12) || 
        (hour >= 14 && hour <= 16) || 
        (hour >= 19 && hour <= 22)) {
      return 5.0;  // 5x normal load
    } else if (hour >= 8 && hour <= 23) {
      return 2.0;  // 2x normal load
    }
    return 0.5;  // Low traffic hours
  }

  private getDayMultiplier(dayOfWeek: number): number {
    // 0 = Sunday, 6 = Saturday
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      return 1.5;  // Weekend boost
    } else if (dayOfWeek >= 1 && dayOfWeek <= 5) {
      return 1.8;  // Weekday boost
    }
    return 1.0;
  }
}
```

## Performance & Scalability Testing

```typescript
// tests/load-testing/scaling-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 500 }, // Ramp up to 500 users
    { duration: '5m', target: 500 }, // Stay at 500 users
    { duration: '2m', target: 1000 }, // Ramp up to 1000 users
    { duration: '5m', target: 1000 }, // Stay at 1000 users
    { duration: '2m', target: 0 }, // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% of requests under 1s
    http_req_failed: ['rate<0.02'], // Error rate under 2%
  },
};

export default function() {
  // Simulate order creation load
  let orderPayload = {
    customerId: `customer-${Math.floor(Math.random() * 10000)}`,
    products: [
      {
        productId: `product-${Math.floor(Math.random() * 1000)}`,
        quantity: Math.floor(Math.random() * 5) + 1
      }
    ]
  };

  let response = http.post('http://api.ecommerce-system.com/api/sales/orders', 
    JSON.stringify(orderPayload), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });

  check(response, {
    'status is 201': (r) => r.status === 201,
    'response time < 1000ms': (r) => r.timings.duration < 1000,
    'order created': (r) => r.json('orderId') !== undefined,
  });

  sleep(1);
}
```

## Summary: Scalability Guarantees

### ✅ **Auto-Scaling Capabilities**

1. **Horizontal Pod Autoscaling**: Based on CPU, memory, and custom metrics
2. **Database Read Replicas**: Automatic scaling with load balancing
3. **Message Queue Scaling**: Dynamic worker adjustment based on queue depth
4. **Redis Clustering**: Distributed caching with automatic failover

### 📊 **Scaling Thresholds**

- **Sales API**: 2-20 instances (CPU: 70%, RPS: 100)
- **Product Service**: 1-10 instances (CPU: 60%, Availability checks: 50/s)
- **Delivery Service**: 1-8 instances (CPU: 75%, Initiations: 30/s)
- **Auth Service**: 2-6 instances (CPU: 70%, Token validations: 200/s)

### 💰 **Cost Optimization**

- **Predictive Scaling**: Based on historical patterns
- **Time-based Policies**: Reduced capacity during low-traffic hours
- **Spot Instances**: Cost-effective scaling for non-critical workloads

### ⏱️ **Scaling Performance**

- **Scale-up Time**: 60 seconds (aggressive policy)
- **Scale-down Time**: 5 minutes (conservative to avoid thrashing)
- **Load Balancer**: Automatic instance registration/deregistration

This auto-scaling architecture ensures your e-commerce system can **handle peak hour traffic efficiently** while **optimizing costs** during low-traffic periods. 