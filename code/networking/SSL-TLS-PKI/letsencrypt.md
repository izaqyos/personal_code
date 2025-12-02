# Let's Encrypt 🔓

> **Free, automated TLS certificates**

## Overview

Let's Encrypt provides free DV certificates via ACME protocol. Certificates valid for 90 days, automated renewal recommended.

## Certbot

### Installation

```bash
# Debian/Ubuntu
sudo apt install certbot

# With nginx plugin
sudo apt install python3-certbot-nginx

# With apache plugin
sudo apt install python3-certbot-apache

# Snap (recommended)
sudo snap install --classic certbot
```

### Get Certificate

```bash
# Standalone (port 80 must be free)
sudo certbot certonly --standalone -d example.com -d www.example.com

# Webroot (server running)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# Nginx plugin (auto-configures)
sudo certbot --nginx -d example.com

# Apache plugin
sudo certbot --apache -d example.com

# DNS challenge (wildcard)
sudo certbot certonly --manual --preferred-challenges dns -d '*.example.com'
```

### Certificate Location

```
/etc/letsencrypt/live/example.com/
├── cert.pem       # Domain certificate
├── chain.pem      # Intermediate CA
├── fullchain.pem  # cert.pem + chain.pem (use this)
└── privkey.pem    # Private key
```

### Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Actual renewal
sudo certbot renew

# Auto-renewal (usually via cron/systemd)
# Check timer
sudo systemctl list-timers | grep certbot
```

### Hooks

```bash
# Reload nginx after renewal
sudo certbot renew --deploy-hook "systemctl reload nginx"

# In renewal config
# /etc/letsencrypt/renewal/example.com.conf
[renewalparams]
deploy_hook = systemctl reload nginx
```

## acme.sh

Alternative ACME client, pure shell script.

```bash
# Install
curl https://get.acme.sh | sh

# Get certificate (standalone)
acme.sh --issue -d example.com --standalone

# Get certificate (webroot)
acme.sh --issue -d example.com -w /var/www/html

# Get certificate (DNS - Cloudflare)
export CF_Token="your_api_token"
acme.sh --issue -d example.com -d '*.example.com' --dns dns_cf

# Install certificate
acme.sh --install-cert -d example.com \
    --key-file /etc/nginx/ssl/key.pem \
    --fullchain-file /etc/nginx/ssl/cert.pem \
    --reloadcmd "systemctl reload nginx"
```

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    
    root /var/www/html;
}
```

## Rate Limits

| Limit | Value |
|-------|-------|
| Certificates per domain | 50/week |
| Duplicate certificates | 5/week |
| Failed validations | 5/hour |
| New orders | 300/3 hours |

## Troubleshooting

```bash
# Check certificate
sudo certbot certificates

# Verbose/debug
sudo certbot certonly -v --dry-run -d example.com

# Delete certificate
sudo certbot delete --cert-name example.com

# Check ACME challenge
curl http://example.com/.well-known/acme-challenge/test
```

---

*Previous: [← PKI](./pki.md) | Back: [SSL-TLS-PKI README](./README.md)*

