# SONET/SDH Optical Transport 💡

> **Synchronous Optical Networking**

## Overview

SONET (North America) and SDH (International) are synchronous TDM standards for fiber optic networks.

## SONET/SDH Rates

| SONET | SDH | Rate | Payload |
|-------|-----|------|---------|
| STS-1/OC-1 | - | 51.84 Mbps | 50.112 Mbps |
| STS-3/OC-3 | STM-1 | 155.52 Mbps | 150.336 Mbps |
| STS-12/OC-12 | STM-4 | 622.08 Mbps | 601.344 Mbps |
| STS-48/OC-48 | STM-16 | 2.488 Gbps | 2.405 Gbps |
| STS-192/OC-192 | STM-64 | 9.953 Gbps | 9.621 Gbps |
| STS-768/OC-768 | STM-256 | 39.813 Gbps | 38.486 Gbps |

```
OC = Optical Carrier (fiber)
STS = Synchronous Transport Signal (electrical)
STM = Synchronous Transport Module (SDH)
```

## SONET Frame Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STS-1 Frame (125 μs)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│           90 columns (bytes)                                                │
│  ┌───────────────────────────────────────────────────────────┐             │
│  │     3 cols    │              87 columns                   │             │
│  ├───────────────┼───────────────────────────────────────────┤   9        │
│  │   Transport   │                                           │   rows     │
│  │   Overhead    │          Synchronous Payload              │            │
│  │   (Section +  │            Envelope (SPE)                 │            │
│  │    Line OH)   │                                           │            │
│  │               │  ┌─────────────────────────────────────┐  │            │
│  │               │  │ Path │      Payload (user data)     │  │            │
│  │               │  │  OH  │                              │  │            │
│  │               │  └─────────────────────────────────────┘  │            │
│  └───────────────┴───────────────────────────────────────────┘             │
│                                                                             │
│  Total: 90 × 9 × 8 bits × 8000 frames/sec = 51.84 Mbps                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Overhead Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SONET Overhead                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Section Overhead (rows 1-3):                                              │
│  ├─ Framing (A1, A2)                                                       │
│  ├─ Section trace (J0)                                                     │
│  ├─ BIP-8 error checking (B1)                                              │
│  └─ Orderwire, user channel, DCC                                           │
│                                                                             │
│  Line Overhead (rows 4-9):                                                 │
│  ├─ Pointer (H1, H2, H3)                                                   │
│  ├─ BIP-8 (B2)                                                             │
│  ├─ APS (K1, K2) - protection switching                                    │
│  └─ DCC, orderwire                                                         │
│                                                                             │
│  Path Overhead (in SPE):                                                   │
│  ├─ Path trace (J1)                                                        │
│  ├─ BIP-8 (B3)                                                             │
│  ├─ Path status (G1)                                                       │
│  └─ Signal label (C2)                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Network Elements

| Element | Function |
|---------|----------|
| STE | Section Terminating Equipment |
| LTE | Line Terminating Equipment |
| PTE | Path Terminating Equipment |
| ADM | Add-Drop Multiplexer |
| DCS | Digital Cross-Connect |
| Regenerator | Amplify/reshape signal |

## Ring Topologies

### UPSR (Unidirectional Path Switched Ring)

```
        ────────►
     A ═══════════ B
     ║             ║
     ║  Working    ║
     ║  (CW)       ║
     ║             ║
     C ═══════════ D
        ◄────────
        Protect (CCW)

• Traffic flows one direction (working)
• Protect path in opposite direction
• Path-level protection
• Simple, good for access networks
```

### BLSR (Bidirectional Line Switched Ring)

```
        ◄────────►
     A ═══════════ B
     ║ ▲         ▼ ║
     ║ Working+    ║
     ║ Protect     ║
     ║             ║
     C ═══════════ D
        ◄────────►

• Half capacity for working, half for protect
• Line-level protection
• More efficient bandwidth usage
• Better for inter-office networks
```

## Virtual Tributaries (VT)

Mapping lower-rate signals into STS-1:

| VT Type | Rate | Carries |
|---------|------|---------|
| VT1.5 | 1.728 Mbps | T1 (1.544 Mbps) |
| VT2 | 2.304 Mbps | E1 (2.048 Mbps) |
| VT3 | 3.456 Mbps | DS1C (3.152 Mbps) |
| VT6 | 6.912 Mbps | DS2 (6.312 Mbps) |

## Modern Evolution

```
SONET/SDH → OTN (Optical Transport Network)

OTN advantages:
• Higher rates (100G, 400G)
• Better management overhead
• FEC (Forward Error Correction)
• Transparent to client signals
• Wavelength switching

OTU rates:
• OTU1: 2.66 Gbps
• OTU2: 10.7 Gbps  
• OTU3: 43 Gbps
• OTU4: 112 Gbps
```

---

*Previous: [← TDM](./tdm.md) | Next: [Fiber →](./fiber.md)*

