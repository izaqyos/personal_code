# X.509 Certificates 📜

> **Digital certificates for identity and encryption**

## Certificate Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        X.509 Certificate                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Version                    (v3 = 2)                                       │
│  Serial Number              (unique per CA)                                │
│  Signature Algorithm        (e.g., sha256WithRSAEncryption)                │
│  Issuer                     (CA that signed this cert)                     │
│  Validity                                                                   │
│    ├─ Not Before            (start date)                                   │
│    └─ Not After             (expiration date)                              │
│  Subject                    (identity being certified)                     │
│  Subject Public Key Info                                                    │
│    ├─ Algorithm             (e.g., RSA, ECDSA)                             │
│    └─ Public Key            (the actual key)                               │
│  Extensions (v3)                                                            │
│    ├─ Key Usage             (digitalSignature, keyEncipherment)            │
│    ├─ Extended Key Usage    (serverAuth, clientAuth)                       │
│    ├─ Subject Alt Name      (additional domains, IPs)                      │
│    ├─ Basic Constraints     (CA:TRUE/FALSE)                                │
│    └─ CRL Distribution      (revocation check URL)                         │
│  Signature                  (CA's signature over above)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Certificate Types

### By Validation Level

| Type | Validation | Use Case |
|------|------------|----------|
| DV (Domain Validation) | Domain ownership | Basic HTTPS |
| OV (Organization Validation) | + Organization verified | Business sites |
| EV (Extended Validation) | + Extensive verification | High-trust sites |

### By Scope

| Type | Covers | Example |
|------|--------|---------|
| Single domain | One domain | www.example.com |
| Wildcard | Domain + subdomains | *.example.com |
| Multi-domain (SAN) | Multiple domains | example.com, example.org |

## File Formats

| Format | Extension | Encoding | Description |
|--------|-----------|----------|-------------|
| PEM | .pem, .crt, .cer | Base64 | Most common, text-based |
| DER | .der, .cer | Binary | Binary format |
| PKCS#7 | .p7b, .p7c | Base64/Binary | Certificate chain |
| PKCS#12 | .p12, .pfx | Binary | Cert + private key |

### PEM Format

```
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiUMA0Gcz...
-----END CERTIFICATE-----
```

## Viewing Certificates

```bash
# View PEM certificate
openssl x509 -in cert.pem -text -noout

# View DER certificate
openssl x509 -in cert.der -inform DER -text -noout

# View from server
echo | openssl s_client -connect host:443 2>/dev/null | openssl x509 -text -noout

# View certificate chain
openssl s_client -connect host:443 -showcerts

# View PKCS#12
openssl pkcs12 -in cert.p12 -info
```

## Certificate Chain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Trust Chain                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐                                                   │
│  │    Root CA          │  Self-signed, in trust store                     │
│  │  (DigiCert Root)    │                                                   │
│  └──────────┬──────────┘                                                   │
│             │ signs                                                         │
│  ┌──────────▼──────────┐                                                   │
│  │  Intermediate CA    │  Signed by root                                  │
│  │ (DigiCert SHA2)     │                                                   │
│  └──────────┬──────────┘                                                   │
│             │ signs                                                         │
│  ┌──────────▼──────────┐                                                   │
│  │   End Entity        │  Your certificate                                │
│  │ (www.example.com)   │  Signed by intermediate                          │
│  └─────────────────────┘                                                   │
│                                                                             │
│  Server sends: End Entity + Intermediate(s)                                │
│  Client has: Root CA in trust store                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Revocation Checking

### CRL (Certificate Revocation List)

```bash
# Get CRL URL from certificate
openssl x509 -in cert.pem -noout -text | grep -A2 "CRL Distribution"

# Download and view CRL
curl -O http://crl.example.com/ca.crl
openssl crl -in ca.crl -inform DER -text -noout
```

### OCSP (Online Certificate Status Protocol)

```bash
# Get OCSP URL
openssl x509 -in cert.pem -noout -ocsp_uri

# Check status
openssl ocsp -issuer chain.pem -cert cert.pem \
    -url http://ocsp.example.com -resp_text
```

## Common Fields

### Subject/Issuer DN

| Field | Meaning | Example |
|-------|---------|---------|
| CN | Common Name | www.example.com |
| O | Organization | Example Inc |
| OU | Organizational Unit | IT Department |
| L | Locality | San Francisco |
| ST | State | California |
| C | Country | US |

### Key Usage

| Usage | Purpose |
|-------|---------|
| digitalSignature | Signing data |
| keyEncipherment | Encrypting keys (RSA key exchange) |
| keyAgreement | DH key agreement |
| keyCertSign | Signing certificates (CA only) |
| cRLSign | Signing CRLs (CA only) |

### Extended Key Usage

| OID | Purpose |
|-----|---------|
| serverAuth | TLS server |
| clientAuth | TLS client |
| codeSigning | Code signing |
| emailProtection | S/MIME |
| timeStamping | Trusted timestamps |

---

*Previous: [← TLS](./tls.md) | Next: [OpenSSL →](./openssl.md)*

