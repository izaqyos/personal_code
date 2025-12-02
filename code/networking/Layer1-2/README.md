# Layer 1 & 2 Technologies 🔌

> **Physical and Data Link Layer Infrastructure**

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OSI Layers 1 & 2                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Layer 2 - Data Link                                                        │
│  ├─ Ethernet (IEEE 802.3)                                                  │
│  ├─ MPLS (label switching)                                                 │
│  ├─ Frame Relay (legacy WAN)                                               │
│  ├─ ATM (Asynchronous Transfer Mode)                                       │
│  └─ PPP (Point-to-Point Protocol)                                          │
│                                                                             │
│  Layer 1 - Physical                                                         │
│  ├─ Fiber Optics (single/multi-mode)                                       │
│  ├─ Copper (twisted pair, coax)                                            │
│  ├─ TDM (E1/T1, SONET/SDH)                                                │
│  └─ Wireless (radio spectrum)                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Contents

| Topic | File | Description |
|-------|------|-------------|
| MPLS | [mpls.md](./mpls.md) | Label switching, VPNs |
| E1/T1 | [tdm.md](./tdm.md) | Digital hierarchies |
| SONET/SDH | [sonet-sdh.md](./sonet-sdh.md) | Optical transport |
| Fiber | [fiber.md](./fiber.md) | Fiber optics |
| Ethernet | [ethernet.md](./ethernet.md) | LAN/WAN Ethernet |

## Speed Reference

### Ethernet

| Standard | Speed | Media |
|----------|-------|-------|
| 10BASE-T | 10 Mbps | Cat 3+ |
| 100BASE-TX | 100 Mbps | Cat 5 |
| 1000BASE-T | 1 Gbps | Cat 5e/6 |
| 10GBASE-T | 10 Gbps | Cat 6a/7 |
| 25GBASE-T | 25 Gbps | Cat 8 |

### Fiber Ethernet

| Standard | Speed | Reach |
|----------|-------|-------|
| 1000BASE-SX | 1 Gbps | 550m MMF |
| 1000BASE-LX | 1 Gbps | 10km SMF |
| 10GBASE-SR | 10 Gbps | 400m MMF |
| 10GBASE-LR | 10 Gbps | 10km SMF |
| 100GBASE-SR4 | 100 Gbps | 100m MMF |
| 100GBASE-LR4 | 100 Gbps | 10km SMF |

### TDM

| Type | Rate | Region |
|------|------|--------|
| T1/DS1 | 1.544 Mbps | North America |
| E1 | 2.048 Mbps | Europe/ROW |
| T3/DS3 | 44.736 Mbps | North America |
| E3 | 34.368 Mbps | Europe |

### SONET/SDH

| SONET | SDH | Rate |
|-------|-----|------|
| OC-1 | - | 51.84 Mbps |
| OC-3 | STM-1 | 155.52 Mbps |
| OC-12 | STM-4 | 622.08 Mbps |
| OC-48 | STM-16 | 2.488 Gbps |
| OC-192 | STM-64 | 9.953 Gbps |
| OC-768 | STM-256 | 39.813 Gbps |

---

*Related: [CCNA Network Fundamentals](../CCNA/modules/01-network-fundamentals/)*

