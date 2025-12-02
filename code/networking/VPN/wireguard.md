# WireGuard VPN ⚡

> **Modern, fast, and simple VPN protocol**

## Overview

WireGuard is a next-generation VPN protocol that is:
- **Fast** - Uses state-of-the-art cryptography
- **Simple** - ~4,000 lines of code (vs 100,000+ for OpenVPN)
- **Secure** - Modern crypto, small attack surface
- **Easy** - Simple configuration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WireGuard vs Others                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Feature        │ WireGuard  │ OpenVPN    │ IPsec                          │
│  ────────────────────────────────────────────────────────────────────────  │
│  Code lines     │ ~4,000     │ ~100,000   │ ~400,000                       │
│  Encryption     │ ChaCha20   │ Various    │ Various                        │
│  Key exchange   │ Curve25519 │ RSA/TLS    │ IKE/DH                         │
│  Performance    │ Excellent  │ Good       │ Good                           │
│  Battery impact │ Low        │ High       │ Medium                         │
│  Roaming        │ Excellent  │ Poor       │ Requires MOBIKE                │
│  Config         │ Simple     │ Complex    │ Very Complex                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Cryptography (Non-Negotiable)

WireGuard uses fixed, modern algorithms:

| Purpose | Algorithm |
|---------|-----------|
| Symmetric Encryption | ChaCha20 |
| Authentication | Poly1305 |
| Key Exchange | Curve25519 (ECDH) |
| Hashing | BLAKE2s |
| Key Derivation | HKDF |

**No cipher negotiation = smaller attack surface**

---

## Installation

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install wireguard wireguard-tools

# RHEL/CentOS 8+
sudo dnf install wireguard-tools

# macOS
brew install wireguard-tools

# Verify
wg --version
```

---

## Key Generation

```bash
# Generate private key
wg genkey > privatekey

# Generate public key from private
wg pubkey < privatekey > publickey

# Generate both at once
wg genkey | tee privatekey | wg pubkey > publickey

# Generate preshared key (optional, extra security)
wg genpsk > presharedkey

# View keys
cat privatekey
cat publickey
```

---

## Server Configuration

### Basic Server Setup

```bash
# /etc/wireguard/wg0.conf

[Interface]
# Server's private key
PrivateKey = SERVER_PRIVATE_KEY_HERE

# Server's VPN IP address
Address = 10.0.0.1/24

# Port to listen on
ListenPort = 51820

# Optional: Run commands on interface up/down
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# DNS for clients (optional)
DNS = 8.8.8.8, 8.8.4.4

# Save config on shutdown
SaveConfig = false

[Peer]
# Client 1
PublicKey = CLIENT1_PUBLIC_KEY_HERE
# Optional: Preshared key for post-quantum resistance
PresharedKey = PRESHARED_KEY_HERE
# Client's allowed IPs (what IPs can this peer send from)
AllowedIPs = 10.0.0.2/32

[Peer]
# Client 2
PublicKey = CLIENT2_PUBLIC_KEY_HERE
AllowedIPs = 10.0.0.3/32
```

### Enable IP Forwarding

```bash
# Enable forwarding
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding=1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Start Server

```bash
# Start interface
sudo wg-quick up wg0

# Enable on boot
sudo systemctl enable wg-quick@wg0

# Check status
sudo wg show
```

---

## Client Configuration

### Basic Client Setup

```bash
# /etc/wireguard/wg0.conf

[Interface]
# Client's private key
PrivateKey = CLIENT_PRIVATE_KEY_HERE

# Client's VPN IP address
Address = 10.0.0.2/32

# DNS servers to use when connected
DNS = 8.8.8.8, 8.8.4.4

[Peer]
# Server's public key
PublicKey = SERVER_PUBLIC_KEY_HERE

# Optional: Preshared key (must match server)
PresharedKey = PRESHARED_KEY_HERE

# Server's public IP and port
Endpoint = vpn.example.com:51820

# Route all traffic through VPN (0.0.0.0/0) or specific subnets
AllowedIPs = 0.0.0.0/0, ::/0

# Keep connection alive (important behind NAT)
PersistentKeepalive = 25
```

### Connect Client

```bash
# Connect
sudo wg-quick up wg0

# Disconnect
sudo wg-quick down wg0

# Check status
sudo wg show
```

---

## Site-to-Site Configuration

### Site A (10.10.1.0/24) ↔ Site B (10.10.2.0/24)

**Site A Configuration:**
```bash
# /etc/wireguard/wg0.conf (Site A)

[Interface]
PrivateKey = SITE_A_PRIVATE_KEY
Address = 172.16.0.1/30
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT

[Peer]
# Site B
PublicKey = SITE_B_PUBLIC_KEY
Endpoint = site-b.example.com:51820
AllowedIPs = 172.16.0.2/32, 10.10.2.0/24
PersistentKeepalive = 25
```

**Site B Configuration:**
```bash
# /etc/wireguard/wg0.conf (Site B)

[Interface]
PrivateKey = SITE_B_PRIVATE_KEY
Address = 172.16.0.2/30
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT

[Peer]
# Site A
PublicKey = SITE_A_PUBLIC_KEY
Endpoint = site-a.example.com:51820
AllowedIPs = 172.16.0.1/32, 10.10.1.0/24
PersistentKeepalive = 25
```

---

## Mobile Configuration

### Generate QR Code for Mobile

```bash
# Install qrencode
sudo apt install qrencode

# Generate QR code from config
qrencode -t ansiutf8 < /etc/wireguard/client-mobile.conf

# Generate PNG file
qrencode -t png -o client-mobile.png < /etc/wireguard/client-mobile.conf
```

### iOS/Android Apps
- Download WireGuard app from App Store / Play Store
- Scan QR code or import config file

---

## Management Commands

```bash
# Show all interfaces
sudo wg show

# Show specific interface
sudo wg show wg0

# Show only public keys
sudo wg show wg0 public-key

# Add peer on the fly
sudo wg set wg0 peer CLIENT_PUBKEY allowed-ips 10.0.0.5/32

# Remove peer
sudo wg set wg0 peer CLIENT_PUBKEY remove

# Show transfer statistics
sudo wg show wg0 transfer

# Show latest handshake times
sudo wg show wg0 latest-handshakes
```

---

## Automated Client Generation Script

```bash
#!/bin/bash
# add-client.sh

CLIENT_NAME=$1
SERVER_PUBKEY="YOUR_SERVER_PUBLIC_KEY"
SERVER_ENDPOINT="vpn.example.com:51820"
DNS="8.8.8.8, 8.8.4.4"

if [ -z "$CLIENT_NAME" ]; then
    echo "Usage: $0 <client-name>"
    exit 1
fi

# Get next available IP
LAST_IP=$(grep -oP 'AllowedIPs = 10\.0\.0\.\K\d+' /etc/wireguard/wg0.conf | sort -n | tail -1)
NEXT_IP=$((LAST_IP + 1))

# Generate keys
CLIENT_PRIVATE=$(wg genkey)
CLIENT_PUBLIC=$(echo "$CLIENT_PRIVATE" | wg pubkey)
PSK=$(wg genpsk)

# Create client config
mkdir -p ~/wireguard-clients
cat > ~/wireguard-clients/${CLIENT_NAME}.conf << EOF
[Interface]
PrivateKey = ${CLIENT_PRIVATE}
Address = 10.0.0.${NEXT_IP}/32
DNS = ${DNS}

[Peer]
PublicKey = ${SERVER_PUBKEY}
PresharedKey = ${PSK}
Endpoint = ${SERVER_ENDPOINT}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

# Add peer to server
sudo wg set wg0 peer ${CLIENT_PUBLIC} preshared-key <(echo "$PSK") allowed-ips 10.0.0.${NEXT_IP}/32

# Save server config
sudo wg-quick save wg0

# Generate QR code
qrencode -t ansiutf8 < ~/wireguard-clients/${CLIENT_NAME}.conf

echo "Client config: ~/wireguard-clients/${CLIENT_NAME}.conf"
echo "Client IP: 10.0.0.${NEXT_IP}"
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No handshake | Firewall blocking UDP 51820 | Open port |
| Handshake but no traffic | AllowedIPs misconfigured | Check routing |
| High latency | Missing PersistentKeepalive | Add keepalive |
| Connection drops | NAT timeout | Reduce keepalive |
| DNS not working | DNS not pushed | Check DNS setting |

### Debug Commands

```bash
# Check interface
ip link show wg0
ip addr show wg0
ip route show

# Check wireguard status
sudo wg show wg0

# Test connectivity
ping 10.0.0.1  # Server's VPN IP

# Check firewall
sudo iptables -L -v -n
sudo iptables -t nat -L -v -n

# Debug with tcpdump
sudo tcpdump -i eth0 udp port 51820

# Kernel logs
dmesg | grep wireguard
journalctl -u wg-quick@wg0
```

---

## Security Best Practices

1. **Use preshared keys** - Post-quantum resistance
2. **Restrict AllowedIPs** - Only necessary ranges
3. **Rotate keys periodically** - Generate new keypairs
4. **Firewall the interface** - Restrict what's accessible
5. **Monitor connections** - Check for unknown peers
6. **Keep updated** - WireGuard receives security fixes

---

*Previous: [← OpenVPN](./openvpn.md) | Next: [SSL VPN →](./ssl-vpn.md)*

