# SSL/TLS VPN Guide 🔐

> **HTTPS-based VPNs for web access and remote connectivity**

## Overview

SSL VPNs use TLS (the same encryption as HTTPS) to provide secure remote access, often without requiring dedicated client software.

## Types of SSL VPN

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SSL VPN Types                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Clientless (Portal):              Full Tunnel (Client):                   │
│  ┌─────────────┐                   ┌─────────────┐                         │
│  │  Browser    │                   │ SSL Client  │                         │
│  │  (HTTPS)    │                   │ (Software)  │                         │
│  └──────┬──────┘                   └──────┬──────┘                         │
│         │                                 │                                │
│         ▼                                 ▼                                │
│  ┌─────────────┐                   ┌─────────────┐                         │
│  │ Web Portal  │                   │ Full Network│                         │
│  │ - Webmail   │                   │ Access via  │                         │
│  │ - File share│                   │ Virtual NIC │                         │
│  │ - Web apps  │                   └─────────────┘                         │
│  └─────────────┘                                                           │
│                                                                             │
│  Pros: No client install           Pros: Full network access              │
│  Cons: Limited to web apps         Cons: Requires client                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Common SSL VPN Solutions

| Solution | Type | Platform |
|----------|------|----------|
| Cisco AnyConnect | Full tunnel | Enterprise |
| Palo Alto GlobalProtect | Full tunnel | Enterprise |
| Fortinet FortiClient | Full tunnel | Enterprise |
| OpenConnect | Full tunnel | Open source (AnyConnect compatible) |
| sslh | Multiplexer | Linux |

---

## OpenConnect (AnyConnect-Compatible)

### Installation

```bash
# Client
sudo apt install openconnect network-manager-openconnect-gnome

# Server (ocserv)
sudo apt install ocserv
```

### Connect to Cisco AnyConnect Server

```bash
# Basic connection
sudo openconnect vpn.company.com

# With username
sudo openconnect -u username vpn.company.com

# With certificate
sudo openconnect -c client.pem vpn.company.com

# Background mode
sudo openconnect --background vpn.company.com
```

### ocserv Server Configuration

```bash
# /etc/ocserv/ocserv.conf

# Authentication
auth = "plain[passwd=/etc/ocserv/passwd]"

# Networking
tcp-port = 443
udp-port = 443
run-as-user = nobody
run-as-group = nogroup

# Certificates
server-cert = /etc/ocserv/server-cert.pem
server-key = /etc/ocserv/server-key.pem
ca-cert = /etc/ocserv/ca-cert.pem

# VPN settings
ipv4-network = 10.10.10.0
ipv4-netmask = 255.255.255.0
dns = 8.8.8.8

# Routes to push
route = 192.168.1.0/24
```

---

## Stunnel (SSL Wrapper)

Wrap any TCP service in TLS:

```bash
# /etc/stunnel/stunnel.conf

[ssh-over-ssl]
accept = 443
connect = 127.0.0.1:22
cert = /etc/stunnel/stunnel.pem
```

---

*Previous: [← WireGuard](./wireguard.md) | Back: [VPN README](./README.md)*

