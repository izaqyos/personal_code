# OpenSSL Commands 🔧

> **The Swiss Army knife for SSL/TLS**

## Generate Keys

```bash
# RSA key (2048 bit)
openssl genrsa -out private.key 2048

# RSA key with encryption
openssl genrsa -aes256 -out private.key 4096

# ECDSA key
openssl ecparam -genkey -name prime256v1 -out private.key

# Ed25519 key
openssl genpkey -algorithm Ed25519 -out private.key

# View key
openssl rsa -in private.key -text -noout
openssl ec -in private.key -text -noout

# Extract public key
openssl rsa -in private.key -pubout -out public.key
```

## Certificate Signing Requests (CSR)

```bash
# Generate CSR (interactive)
openssl req -new -key private.key -out request.csr

# Generate key + CSR together
openssl req -new -newkey rsa:2048 -nodes -keyout private.key -out request.csr

# CSR with SAN (config file)
openssl req -new -key private.key -out request.csr -config san.cnf

# View CSR
openssl req -in request.csr -text -noout

# Verify CSR
openssl req -in request.csr -verify
```

### SAN Config File

```ini
# san.cnf
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
CN = example.com
O = Example Inc
C = US

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
DNS.3 = api.example.com
IP.1 = 192.168.1.1
```

## Self-Signed Certificates

```bash
# Quick self-signed (1 year)
openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout key.pem -out cert.pem -days 365 \
    -subj "/CN=localhost"

# Self-signed with SAN
openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout key.pem -out cert.pem -days 365 \
    -config san.cnf -extensions v3_req

# From existing key + CSR
openssl x509 -req -in request.csr -signkey private.key \
    -out certificate.crt -days 365
```

## Certificate Operations

```bash
# View certificate
openssl x509 -in cert.pem -text -noout

# View specific fields
openssl x509 -in cert.pem -noout -subject
openssl x509 -in cert.pem -noout -issuer
openssl x509 -in cert.pem -noout -dates
openssl x509 -in cert.pem -noout -serial
openssl x509 -in cert.pem -noout -fingerprint -sha256

# Check expiration
openssl x509 -in cert.pem -noout -checkend 86400  # expires in 24h?

# Get certificate from server
echo | openssl s_client -connect host:443 2>/dev/null | \
    openssl x509 -out cert.pem
```

## Format Conversions

```bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER to PEM
openssl x509 -in cert.der -inform DER -out cert.pem

# PEM to PKCS#12
openssl pkcs12 -export -out cert.p12 \
    -inkey private.key -in cert.pem -certfile chain.pem

# PKCS#12 to PEM
openssl pkcs12 -in cert.p12 -out combined.pem -nodes

# Extract from PKCS#12
openssl pkcs12 -in cert.p12 -nocerts -out key.pem      # Key only
openssl pkcs12 -in cert.p12 -clcerts -nokeys -out cert.pem  # Cert only

# PKCS#7 to PEM
openssl pkcs7 -in cert.p7b -print_certs -out certs.pem
```

## Verification

```bash
# Verify cert against CA
openssl verify -CAfile ca.pem cert.pem

# Verify chain
openssl verify -CAfile root.pem -untrusted intermediate.pem cert.pem

# Check key matches certificate
openssl x509 -in cert.pem -noout -modulus | openssl md5
openssl rsa -in key.pem -noout -modulus | openssl md5
# Should match

# Check CSR matches key
openssl req -in request.csr -noout -modulus | openssl md5
openssl rsa -in key.pem -noout -modulus | openssl md5
```

## TLS Testing

```bash
# Connect to server
openssl s_client -connect host:443

# With SNI (required for most servers)
openssl s_client -connect host:443 -servername hostname

# Show certificate chain
openssl s_client -connect host:443 -showcerts

# Specific TLS version
openssl s_client -connect host:443 -tls1_2
openssl s_client -connect host:443 -tls1_3

# Test specific cipher
openssl s_client -connect host:443 -cipher 'ECDHE-RSA-AES256-GCM-SHA384'

# STARTTLS
openssl s_client -connect host:25 -starttls smtp
openssl s_client -connect host:143 -starttls imap
```

## Encryption/Decryption

```bash
# Encrypt file with password
openssl enc -aes-256-cbc -salt -in file.txt -out file.enc

# Decrypt
openssl enc -aes-256-cbc -d -in file.enc -out file.txt

# Encrypt with public key
openssl rsautl -encrypt -pubin -inkey public.key -in file.txt -out file.enc

# Decrypt with private key
openssl rsautl -decrypt -inkey private.key -in file.enc -out file.txt
```

## Hash/Digest

```bash
# File hash
openssl dgst -sha256 file.txt
openssl sha256 file.txt

# Sign file
openssl dgst -sha256 -sign private.key -out signature.bin file.txt

# Verify signature
openssl dgst -sha256 -verify public.key -signature signature.bin file.txt
```

---

*Previous: [← Certificates](./certificates.md) | Next: [PKI →](./pki.md)*

