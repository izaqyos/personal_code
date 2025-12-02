# TLS Fundamentals 🔒

> **Transport Layer Security Protocol**

## TLS Record Protocol

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        TLS Record Format                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┬──────────┬──────────┬─────────────────────────────────┐      │
│  │ Content  │ Version  │ Length   │          Fragment               │      │
│  │  Type    │ (2 bytes)│ (2 bytes)│      (max 16KB)                │      │
│  │ (1 byte) │          │          │                                 │      │
│  └──────────┴──────────┴──────────┴─────────────────────────────────┘      │
│                                                                             │
│  Content Types:                                                             │
│    20 = ChangeCipherSpec                                                   │
│    21 = Alert                                                              │
│    22 = Handshake                                                          │
│    23 = Application Data                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Key Exchange Methods

| Method | Description | Forward Secrecy |
|--------|-------------|-----------------|
| RSA | Encrypt premaster with server's public key | No |
| DHE | Diffie-Hellman Ephemeral | Yes |
| ECDHE | Elliptic Curve DHE | Yes |
| PSK | Pre-Shared Key | Depends |

### Forward Secrecy

```
Without FS (RSA key exchange):
- Server's private key compromised
- All past traffic can be decrypted

With FS (DHE/ECDHE):
- Unique key per session
- Past traffic remains secure even if long-term key compromised
```

## Cipher Suites

### Recommended (TLS 1.3)

```
TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
TLS_AES_128_GCM_SHA256
```

### Recommended (TLS 1.2)

```
TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256
TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

### Avoid

```
# No forward secrecy
TLS_RSA_WITH_*

# Weak encryption
*_RC4_*
*_3DES_*
*_DES_*
*_NULL_*
*_EXPORT_*

# Weak hash
*_MD5
*_SHA (SHA-1 for signatures)
```

## TLS 1.3 Changes

| Removed | Reason |
|---------|--------|
| RSA key exchange | No forward secrecy |
| Static DH | No forward secrecy |
| CBC mode ciphers | Padding oracle attacks |
| RC4, 3DES | Weak |
| SHA-1 | Weak |
| Compression | CRIME attack |
| Renegotiation | Complex, attack surface |

## Server Configuration

### Nginx

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;

# HSTS
add_header Strict-Transport-Security "max-age=63072000" always;
```

### Apache

```apache
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
SSLHonorCipherOrder off
SSLSessionTickets off

Header always set Strict-Transport-Security "max-age=63072000"
```

## Testing

```bash
# Check TLS version support
openssl s_client -connect host:443 -tls1_2
openssl s_client -connect host:443 -tls1_3

# List supported ciphers
openssl s_client -connect host:443 -cipher 'ALL' 2>/dev/null | grep Cipher

# Full test with testssl.sh
./testssl.sh host:443

# nmap cipher enumeration
nmap --script ssl-enum-ciphers -p 443 host
```

---

*Next: [Certificates →](./certificates.md)*

