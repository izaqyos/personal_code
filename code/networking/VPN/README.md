# VPN Technologies Deep Dive 🔐

> **Comprehensive guide to VPN protocols and implementations**

## Overview

This section covers practical VPN technologies used in modern networks, from enterprise IPsec to consumer-friendly WireGuard.

## VPN Types Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VPN Protocol Comparison                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Protocol    │ Speed    │ Security │ Setup     │ Best For                  │
│  ──────────────────────────────────────────────────────────────────────────│
│  WireGuard   │ ★★★★★   │ ★★★★★   │ ★★★★★    │ Modern, simple VPN         │
│  OpenVPN     │ ★★★☆☆   │ ★★★★★   │ ★★★☆☆    │ Flexible, cross-platform   │
│  IPsec/IKEv2 │ ★★★★☆   │ ★★★★★   │ ★★☆☆☆    │ Enterprise, site-to-site   │
│  L2TP/IPsec  │ ★★★☆☆   │ ★★★★☆   │ ★★★☆☆    │ Native client support      │
│  PPTP        │ ★★★★☆   │ ★☆☆☆☆   │ ★★★★★    │ AVOID - broken crypto      │
│  SSL VPN     │ ★★★☆☆   │ ★★★★☆   │ ★★★★☆    │ Clientless web access      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Contents

| Topic | File | Description |
|-------|------|-------------|
| IPsec Fundamentals | [ipsec.md](./ipsec.md) | IKE, ESP, AH, site-to-site |
| OpenVPN | [openvpn.md](./openvpn.md) | Setup, config, certificates |
| WireGuard | [wireguard.md](./wireguard.md) | Modern VPN setup |
| SSL/TLS VPN | [ssl-vpn.md](./ssl-vpn.md) | HTTPS-based VPNs |
| VPN Troubleshooting | [troubleshooting.md](./troubleshooting.md) | Common issues |

## Architecture Overview

```
                    VPN Architecture Types
                    
Site-to-Site:                       Remote Access:
┌─────────┐         ┌─────────┐    ┌─────────┐         ┌─────────┐
│ Site A  │═════════│ Site B  │    │  User   │═════════│ VPN GW  │
│ Network │ Tunnel  │ Network │    │ Client  │ Tunnel  │ Server  │
└─────────┘         └─────────┘    └─────────┘         └────┬────┘
                                                            │
                                                    ┌───────┴───────┐
                                                    │   Corporate   │
                                                    │   Network     │
                                                    └───────────────┘

Hub-and-Spoke:                      Full Mesh:
       ┌──────┐                     ┌──────┐───────┌──────┐
       │ Hub  │                     │ Site │       │ Site │
       └──┬───┘                     │  A   │       │  B   │
      ╱   │   ╲                     └──┬───┘       └──┬───┘
     ╱    │    ╲                       │╲           ╱│
┌───┴─┐ ┌─┴──┐ ┌┴───┐                  │ ╲         ╱ │
│Spoke│ │Spoke│ │Spoke│                 │  ╲       ╱  │
└─────┘ └────┘ └─────┘                  │   ╲     ╱   │
                                    ┌───┴────╲─╱──────┴───┐
                                    │       Site C        │
                                    └─────────────────────┘
```

## Quick Start Guides

### For Home/Personal Use
→ Start with [WireGuard](./wireguard.md) - simplest, fastest

### For Enterprise
→ Start with [IPsec](./ipsec.md) - industry standard

### For Flexibility/Compatibility  
→ Start with [OpenVPN](./openvpn.md) - works everywhere

---

## Port Reference

| Protocol | Ports | Notes |
|----------|-------|-------|
| IPsec IKE | UDP 500 | Key exchange |
| IPsec NAT-T | UDP 4500 | NAT traversal |
| IPsec ESP | IP Protocol 50 | Encrypted payload |
| IPsec AH | IP Protocol 51 | Auth only (rare) |
| OpenVPN | UDP 1194 (default) | Can use TCP 443 |
| WireGuard | UDP 51820 (default) | Configurable |
| L2TP | UDP 1701 | Usually with IPsec |
| SSTP | TCP 443 | Microsoft SSL VPN |

---

*Related: [CCNP Virtualization Module](../CCNP/modules/02-virtualization/)*

