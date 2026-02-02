# Proxies

Intermediary servers that sit between clients and backend servers.

## Types of Proxies

### Forward Proxy

Sits between clients and the internet.

```
Client → Forward Proxy → Internet → Server
```

**Use cases:**
- Anonymity (hide client IP)
- Content filtering
- Caching
- Access control
- Bypassing restrictions

**Examples:** Squid, corporate proxies

### Reverse Proxy

Sits between internet and backend servers.

```
Client → Internet → Reverse Proxy → Server
```

**Use cases:**
- Load balancing
- SSL termination
- Caching
- Compression
- Security (hide server details)

**Examples:** NGINX, HAProxy, Envoy

## Comparison

| Aspect | Forward Proxy | Reverse Proxy |
|--------|---------------|---------------|
| Protects | Clients | Servers |
| Client awareness | Knows about proxy | Unaware of proxy |
| Server awareness | Unaware of clients | Knows about clients |
| Configuration | Client-side | Server-side |

## Reverse Proxy Functions

### Load Balancing

```
                    ┌──────────────┐
Client ────────────>│Reverse Proxy │────> Server 1
                    │              │────> Server 2
                    │              │────> Server 3
                    └──────────────┘
```

### SSL Termination

```
Client ─[HTTPS]─> Reverse Proxy ─[HTTP]─> Backend
```

**Benefits:**
- Centralized certificate management
- Offload encryption from backends
- Simpler backend configuration

### Caching

```
Reverse Proxy Cache
┌─────────────────────────────────┐
│ /api/products → cached response │
│ /images/* → cached files        │
└─────────────────────────────────┘
```

### Compression

```
Backend → Reverse Proxy (gzip/brotli) → Client
```

### Request Buffering

```
Slow Client ──[chunk]──> Proxy ──[full request]──> Backend
                              (buffer)
```

Protects backend from slow clients.

### URL Rewriting

```
/old-api/users → /api/v2/users
/blog/post-slug → /articles?slug=post-slug
```

## NGINX Configuration Example

```nginx
upstream backend {
    server backend1:8080 weight=3;
    server backend2:8080 weight=1;
    server backend3:8080 backup;
}

server {
    listen 443 ssl;
    server_name example.com;
    
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    
    # Caching
    proxy_cache_path /var/cache/nginx levels=1:2 
                     keys_zone=cache:10m max_size=10g;
    
    location /api/ {
        proxy_pass http://backend;
        proxy_cache cache;
        proxy_cache_valid 200 1h;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static/ {
        root /var/www;
        expires 30d;
    }
}
```

## Sidecar Proxy Pattern

Proxy deployed alongside each service instance.

```
┌─────────────────────────────────┐
│ Pod                             │
│ ┌─────────┐     ┌─────────────┐ │
│ │ Service │◄───►│Sidecar Proxy│◄──── Network
│ └─────────┘     └─────────────┘ │
└─────────────────────────────────┘
```

**Use cases:**
- Service mesh (Istio, Linkerd)
- mTLS between services
- Observability
- Traffic management

**Examples:** Envoy (in Istio), Linkerd-proxy

## Transparent Proxy

Intercepts traffic without client configuration.

```
Client ───> Router ───> Transparent Proxy ───> Internet
           (redirect)
```

**Use cases:**
- Corporate network monitoring
- ISP caching
- Content filtering

## Proxy Protocols

### HTTP/HTTPS Proxy

Standard web proxy using HTTP CONNECT for HTTPS.

```
Client: CONNECT server:443 HTTP/1.1
Proxy:  HTTP/1.1 200 Connection Established
        (tunnel established)
```

### SOCKS Proxy

Generic proxy protocol (not HTTP-specific).

```
SOCKS4: TCP only
SOCKS5: TCP + UDP, authentication
```

### Proxy Protocol

Header for preserving client IP through proxies.

```
PROXY TCP4 192.168.1.1 10.0.0.1 56324 443
(original client info)
```

## Security Considerations

### IP Preservation

```http
X-Forwarded-For: client_ip, proxy1_ip, proxy2_ip
X-Real-IP: client_ip
```

**Caution:** Can be spoofed; trust only from known proxies.

### Request Smuggling

Inconsistent parsing between proxy and backend.

**Mitigation:**
- Use HTTP/2
- Consistent parsing
- Reject ambiguous requests

### Proxy Bypass

Clients bypassing proxy directly.

**Mitigation:**
- Network-level enforcement
- Only allow traffic from proxy IPs

## Performance Considerations

### Connection Pooling

```
Proxy maintains persistent connections to backends
  ↓
Avoids TCP handshake overhead per request
```

### Keep-Alive

```
Client ─[keep-alive]─> Proxy ─[keep-alive]─> Backend
```

### Buffer Sizes

```nginx
proxy_buffer_size 4k;
proxy_buffers 8 16k;
proxy_busy_buffers_size 24k;
```

## Common Proxy Solutions

| Solution | Type | Strengths |
|----------|------|-----------|
| NGINX | Reverse | Performance, configuration |
| HAProxy | Reverse | High availability, L4/L7 |
| Envoy | Sidecar | Service mesh, observability |
| Squid | Forward | Caching, filtering |
| Traefik | Reverse | Docker/K8s integration |
| Apache mod_proxy | Reverse | Apache ecosystem |

## Interview Tips

1. Distinguish forward vs reverse proxy
2. Explain common reverse proxy functions
3. Discuss sidecar pattern for service mesh
4. Address security (IP preservation, smuggling)
5. Consider performance (pooling, buffering)
6. Choose appropriate solution for use case

## Related Topics

- [Load Balancers](load_balancers.md)
- [API Gateway](api_gateway.md)
- [CDN](cdn.md)
