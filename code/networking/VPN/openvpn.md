# OpenVPN Guide 🌐

> **Flexible, cross-platform SSL/TLS VPN solution**

## Overview

OpenVPN is an open-source VPN solution using SSL/TLS for key exchange. It's highly configurable and works on virtually any platform.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OpenVPN Architecture                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Client                        Server                                       │
│  ┌─────────────┐              ┌─────────────┐                              │
│  │ OpenVPN     │──────────────│ OpenVPN     │                              │
│  │ Client      │   TLS/SSL    │ Server      │                              │
│  │             │   Tunnel     │             │                              │
│  │ tun0/tap0   │              │ tun0/tap0   │                              │
│  └─────────────┘              └──────┬──────┘                              │
│                                      │                                      │
│                               ┌──────┴──────┐                              │
│                               │  Internal   │                              │
│                               │  Network    │                              │
│                               └─────────────┘                              │
│                                                                             │
│  Modes:                                                                     │
│  • TUN (Layer 3) - Routed VPN, most common                                │
│  • TAP (Layer 2) - Bridged VPN, for L2 protocols                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Server Installation

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install openvpn easy-rsa

# RHEL/CentOS
sudo yum install epel-release
sudo yum install openvpn easy-rsa

# macOS
brew install openvpn

# Create PKI directory
make-cadir ~/openvpn-ca
cd ~/openvpn-ca
```

### Client Installation

```bash
# Linux
sudo apt install openvpn

# macOS
brew install openvpn
# Or use Tunnelblick GUI

# Windows
# Download from https://openvpn.net/community-downloads/
```

---

## Certificate Authority Setup

### Initialize PKI

```bash
cd ~/openvpn-ca

# Edit vars file
nano vars

# Set these variables:
# set_var EASYRSA_REQ_COUNTRY    "US"
# set_var EASYRSA_REQ_PROVINCE   "California"
# set_var EASYRSA_REQ_CITY       "San Francisco"
# set_var EASYRSA_REQ_ORG        "MyOrg"
# set_var EASYRSA_REQ_EMAIL      "admin@example.com"
# set_var EASYRSA_REQ_OU         "IT"
# set_var EASYRSA_KEY_SIZE       4096
# set_var EASYRSA_CA_EXPIRE      3650
# set_var EASYRSA_CERT_EXPIRE    365

# Initialize PKI
./easyrsa init-pki

# Build CA (will prompt for passphrase)
./easyrsa build-ca
```

### Generate Server Certificate

```bash
# Generate server key and request (no password)
./easyrsa gen-req server nopass

# Sign the request
./easyrsa sign-req server server

# Generate Diffie-Hellman parameters
./easyrsa gen-dh

# Generate TLS auth key (extra security)
openvpn --genkey secret ta.key
```

### Generate Client Certificates

```bash
# For each client
./easyrsa gen-req client1 nopass
./easyrsa sign-req client client1

# Copy files for distribution
# client1.crt, client1.key, ca.crt, ta.key
```

---

## Server Configuration

### Basic Server Config

```bash
# /etc/openvpn/server.conf

# Network
port 1194
proto udp
dev tun

# Certificates
ca /etc/openvpn/ca.crt
cert /etc/openvpn/server.crt
key /etc/openvpn/server.key
dh /etc/openvpn/dh.pem
tls-auth /etc/openvpn/ta.key 0

# VPN subnet
server 10.8.0.0 255.255.255.0

# Routing - push routes to clients
push "route 192.168.1.0 255.255.255.0"
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

# Client isolation
client-to-client

# Persistence
ifconfig-pool-persist /var/log/openvpn/ipp.txt

# Security
cipher AES-256-GCM
auth SHA384
tls-version-min 1.2
tls-cipher TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384

# Logging
status /var/log/openvpn/status.log
log-append /var/log/openvpn/openvpn.log
verb 3

# Performance
keepalive 10 120
comp-lzo no
persist-key
persist-tun

# User/Group (drop privileges)
user nobody
group nogroup
```

### Enable IP Forwarding

```bash
# Enable forwarding
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Configure firewall (iptables)
sudo iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i tun0 -j ACCEPT
sudo iptables -A FORWARD -o tun0 -j ACCEPT

# Save rules
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

### Start Server

```bash
sudo systemctl start openvpn@server
sudo systemctl enable openvpn@server
sudo systemctl status openvpn@server
```

---

## Client Configuration

### Client Config File

```bash
# client.ovpn

client
dev tun
proto udp
remote vpn.example.com 1194
resolv-retry infinite
nobind

# Certificates (inline or file paths)
ca ca.crt
cert client1.crt
key client1.key
tls-auth ta.key 1

# Security
cipher AES-256-GCM
auth SHA384
remote-cert-tls server

# Connection
persist-key
persist-tun
verb 3
```

### Inline Certificates (Single File)

```bash
# client-inline.ovpn

client
dev tun
proto udp
remote vpn.example.com 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-GCM
auth SHA384
key-direction 1
verb 3

<ca>
-----BEGIN CERTIFICATE-----
[CA certificate content]
-----END CERTIFICATE-----
</ca>

<cert>
-----BEGIN CERTIFICATE-----
[Client certificate content]
-----END CERTIFICATE-----
</cert>

<key>
-----BEGIN PRIVATE KEY-----
[Client key content]
-----END PRIVATE KEY-----
</key>

<tls-auth>
-----BEGIN OpenVPN Static key V1-----
[TA key content]
-----END OpenVPN Static key V1-----
</tls-auth>
```

### Connect Client

```bash
# Linux
sudo openvpn --config client.ovpn

# As a service
sudo cp client.ovpn /etc/openvpn/client.conf
sudo systemctl start openvpn@client
```

---

## Advanced Configurations

### Client-Specific Configuration (CCD)

```bash
# Server config add:
# client-config-dir /etc/openvpn/ccd

# /etc/openvpn/ccd/client1
ifconfig-push 10.8.0.10 10.8.0.9
push "route 192.168.100.0 255.255.255.0"
```

### Two-Factor Authentication

```bash
# Using google-authenticator
# Server config add:
plugin /usr/lib/openvpn/openvpn-plugin-auth-pam.so openvpn

# /etc/pam.d/openvpn
auth required pam_google_authenticator.so
auth required pam_permit.so
account required pam_permit.so
```

### TCP Mode (For Restrictive Firewalls)

```bash
# Server
proto tcp
port 443

# Client
proto tcp
remote vpn.example.com 443
```

---

## Automated Client Script

```bash
#!/bin/bash
# generate-client.sh

CLIENT=$1
if [ -z "$CLIENT" ]; then
    echo "Usage: $0 <client-name>"
    exit 1
fi

cd ~/openvpn-ca
./easyrsa gen-req $CLIENT nopass
./easyrsa sign-req client $CLIENT

# Create .ovpn file
cat > ~/clients/$CLIENT.ovpn << EOF
client
dev tun
proto udp
remote vpn.example.com 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-GCM
auth SHA384
key-direction 1
verb 3

<ca>
$(cat ~/openvpn-ca/pki/ca.crt)
</ca>

<cert>
$(cat ~/openvpn-ca/pki/issued/$CLIENT.crt)
</cert>

<key>
$(cat ~/openvpn-ca/pki/private/$CLIENT.key)
</key>

<tls-auth>
$(cat ~/openvpn-ca/ta.key)
</tls-auth>
EOF

echo "Client config created: ~/clients/$CLIENT.ovpn"
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| TLS handshake failed | Certificate mismatch | Verify CA/certs |
| No route to host | Firewall blocking | Open UDP 1194 |
| Connection timeout | Wrong server IP/port | Check remote directive |
| Auth failed | Wrong credentials | Regenerate certs |
| No internet via VPN | Missing NAT rule | Add MASQUERADE rule |

### Debug Commands

```bash
# Server logs
sudo tail -f /var/log/openvpn/openvpn.log

# Verbose client
sudo openvpn --config client.ovpn --verb 6

# Test connectivity
sudo openvpn --config client.ovpn --ping 8.8.8.8

# Check tunnel interface
ip addr show tun0
ip route show

# Verify certificates
openssl x509 -in server.crt -text -noout
openssl verify -CAfile ca.crt server.crt
```

---

## Performance Tuning

```bash
# Server optimizations

# Increase buffer sizes
sndbuf 393216
rcvbuf 393216
push "sndbuf 393216"
push "rcvbuf 393216"

# Fragment large packets
fragment 1400
mssfix 1400

# Use fast cipher
cipher AES-128-GCM  # Faster than AES-256

# Multi-threading (OpenVPN 2.5+)
# Run multiple instances with different ports
```

---

*Previous: [← IPsec](./ipsec.md) | Next: [WireGuard →](./wireguard.md)*

