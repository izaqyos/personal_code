# PKI (Public Key Infrastructure) 🏛️

> **Building and managing Certificate Authorities**

## PKI Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PKI Architecture                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│  │   Root CA   │     │ Registration│     │   CRL/OCSP  │                  │
│  │  (offline)  │     │  Authority  │     │   Responder │                  │
│  └──────┬──────┘     └──────┬──────┘     └─────────────┘                  │
│         │                   │                                               │
│  ┌──────▼──────┐     ┌──────▼──────┐                                       │
│  │Intermediate │     │ Validation  │                                       │
│  │     CA      │     │  (verify    │                                       │
│  │  (online)   │     │  identity)  │                                       │
│  └──────┬──────┘     └─────────────┘                                       │
│         │                                                                   │
│  ┌──────▼──────┐                                                           │
│  │ End Entity  │                                                           │
│  │ Certificates│                                                           │
│  └─────────────┘                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Create Private CA

### Root CA

```bash
# Create directory structure
mkdir -p ca/{certs,crl,newcerts,private}
chmod 700 ca/private
touch ca/index.txt
echo 1000 > ca/serial

# Generate root key
openssl genrsa -aes256 -out ca/private/ca.key 4096
chmod 400 ca/private/ca.key

# Create root certificate
openssl req -config ca.cnf -key ca/private/ca.key \
    -new -x509 -days 7300 -sha256 -extensions v3_ca \
    -out ca/certs/ca.crt

# Verify
openssl x509 -in ca/certs/ca.crt -text -noout
```

### CA Config (ca.cnf)

```ini
[ca]
default_ca = CA_default

[CA_default]
dir               = ./ca
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
private_key       = $dir/private/ca.key
certificate       = $dir/certs/ca.crt
crlnumber         = $dir/crlnumber
crl               = $dir/crl/ca.crl
default_md        = sha256
default_days      = 365
preserve          = no
policy            = policy_strict

[policy_strict]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
commonName              = supplied

[req]
distinguished_name = req_distinguished_name
x509_extensions    = v3_ca

[req_distinguished_name]
countryName                     = Country
stateOrProvinceName             = State
organizationName                = Organization
commonName                      = Common Name

[v3_ca]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[v3_intermediate_ca]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[server_cert]
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
```

### Intermediate CA

```bash
# Create intermediate key
openssl genrsa -aes256 -out ca/intermediate/private/intermediate.key 4096

# Create CSR
openssl req -config intermediate.cnf -new -sha256 \
    -key ca/intermediate/private/intermediate.key \
    -out ca/intermediate/csr/intermediate.csr

# Sign with root CA
openssl ca -config ca.cnf -extensions v3_intermediate_ca \
    -days 3650 -notext -md sha256 \
    -in ca/intermediate/csr/intermediate.csr \
    -out ca/intermediate/certs/intermediate.crt

# Create chain file
cat ca/intermediate/certs/intermediate.crt ca/certs/ca.crt > ca/intermediate/certs/chain.crt
```

### Sign Server Certificate

```bash
# Generate server key
openssl genrsa -out server.key 2048

# Create CSR
openssl req -new -key server.key -out server.csr \
    -subj "/CN=server.example.com"

# Sign with intermediate CA
openssl ca -config intermediate.cnf -extensions server_cert \
    -days 365 -notext -md sha256 \
    -in server.csr -out server.crt

# Create full chain for server
cat server.crt ca/intermediate/certs/intermediate.crt > server-chain.crt
```

## Certificate Revocation

### Create CRL

```bash
# Initialize CRL number
echo 1000 > ca/crlnumber

# Generate CRL
openssl ca -config ca.cnf -gencrl -out ca/crl/ca.crl

# View CRL
openssl crl -in ca/crl/ca.crl -text -noout
```

### Revoke Certificate

```bash
# Revoke
openssl ca -config ca.cnf -revoke cert.crt -crl_reason keyCompromise

# Regenerate CRL
openssl ca -config ca.cnf -gencrl -out ca/crl/ca.crl
```

## Tools

### Easy-RSA

```bash
# Initialize
./easyrsa init-pki

# Build CA
./easyrsa build-ca

# Generate server cert
./easyrsa gen-req server nopass
./easyrsa sign-req server server

# Generate client cert
./easyrsa gen-req client nopass
./easyrsa sign-req client client
```

### cfssl

```bash
# Initialize CA
cfssl gencert -initca ca-csr.json | cfssljson -bare ca

# Generate certificate
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
    -config=config.json -profile=server \
    server-csr.json | cfssljson -bare server
```

---

*Previous: [← OpenSSL](./openssl.md) | Next: [Let's Encrypt →](./letsencrypt.md)*

