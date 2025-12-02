# Fiber Optics 🔦

> **Light-based data transmission**

## Fiber Types

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Single-Mode vs Multi-Mode Fiber                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Single-Mode Fiber (SMF)                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ ═══════════════════════════════════════════════════════════════ │       │
│  │                    One light path (mode)                         │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│  • Core: 8-10 μm                                                           │
│  • Cladding: 125 μm                                                        │
│  • Wavelength: 1310nm, 1550nm                                              │
│  • Distance: Up to 100+ km                                                 │
│  • Color code: Yellow jacket                                               │
│                                                                             │
│  Multi-Mode Fiber (MMF)                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │ ══╲═══╱═══╲═══╱═══╲═══╱═══╲═══╱═══╲═══╱═══╲═══╱═══╲═══╱═════ │       │
│  │    Multiple light paths (modes)                                  │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│  • Core: 50 μm or 62.5 μm                                                  │
│  • Cladding: 125 μm                                                        │
│  • Wavelength: 850nm, 1300nm                                               │
│  • Distance: Up to ~500m (OM4)                                             │
│  • Color code: Orange (OM1/OM2), Aqua (OM3/OM4)                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Multi-Mode Categories

| Type | Core | Bandwidth | 10G Distance | Color |
|------|------|-----------|--------------|-------|
| OM1 | 62.5 μm | 200 MHz·km | 33m | Orange |
| OM2 | 50 μm | 500 MHz·km | 82m | Orange |
| OM3 | 50 μm | 2000 MHz·km | 300m | Aqua |
| OM4 | 50 μm | 4700 MHz·km | 400m | Aqua |
| OM5 | 50 μm | 28000 MHz·km | 400m | Lime Green |

## Connectors

| Connector | Description | Use Case |
|-----------|-------------|----------|
| SC | Square, push-pull | Enterprise, data center |
| LC | Small form factor | High density, SFP |
| ST | Bayonet twist | Legacy networks |
| FC | Threaded | Test equipment |
| MPO/MTP | Multi-fiber (12/24) | High speed, parallel |

### Polish Types

| Type | Return Loss | Use |
|------|-------------|-----|
| PC (Physical Contact) | -30 dB | MMF |
| UPC (Ultra PC) | -50 dB | SMF data |
| APC (Angled PC) | -60 dB | SMF, analog, CATV |

```
APC has 8° angle - DO NOT mix with UPC!
APC = Green connector
```

## Transceivers

### Form Factors

| Type | Speed | Notes |
|------|-------|-------|
| SFP | 1G | Most common |
| SFP+ | 10G | Same size as SFP |
| SFP28 | 25G | Same size |
| QSFP+ | 40G | 4 lanes |
| QSFP28 | 100G | 4×25G |
| QSFP-DD | 400G | 8 lanes |

### Common SFP Types

| Type | Wavelength | Fiber | Distance |
|------|------------|-------|----------|
| SX | 850nm | MMF | 550m |
| LX | 1310nm | SMF | 10km |
| EX | 1310nm | SMF | 40km |
| ZX | 1550nm | SMF | 80km |
| BX | BiDi | SMF | 10-80km |
| CWDM/DWDM | Various | SMF | Long haul |

## WDM (Wavelength Division Multiplexing)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WDM - Multiple λ on One Fiber                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  λ1 (1530nm) ────┐                         ┌──── λ1 (1530nm)              │
│  λ2 (1531nm) ────┼──► MUX ═══════ DEMUX ◄──┼──── λ2 (1531nm)              │
│  λ3 (1532nm) ────┤     (single fiber)      ├──── λ3 (1532nm)              │
│  λ4 (1533nm) ────┘                         └──── λ4 (1533nm)              │
│                                                                             │
│  CWDM (Coarse WDM):                                                        │
│  • 20nm spacing                                                            │
│  • 8-18 channels                                                           │
│  • Lower cost                                                              │
│  • Shorter distance                                                        │
│                                                                             │
│  DWDM (Dense WDM):                                                         │
│  • 0.8nm (100 GHz) or 0.4nm (50 GHz) spacing                              │
│  • 40-96+ channels                                                         │
│  • C-band (1530-1565nm), L-band (1565-1625nm)                             │
│  • Long haul with amplifiers                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Optical Amplifiers

| Type | Description |
|------|-------------|
| EDFA | Erbium-Doped Fiber Amplifier (C/L-band) |
| Raman | Distributed amplification |
| SOA | Semiconductor Optical Amplifier |

## Loss Budget Calculation

```
Total Loss = Fiber Loss + Connector Loss + Splice Loss + Margin

Example:
• Fiber: 0.35 dB/km × 10 km = 3.5 dB
• Connectors: 0.5 dB × 4 = 2.0 dB  
• Splices: 0.1 dB × 2 = 0.2 dB
• Margin: 3 dB
• Total: 8.7 dB

Transceiver budget must exceed total loss
```

## Testing Tools

| Tool | Purpose |
|------|---------|
| Power Meter | Measure light level |
| Light Source | Generate test signal |
| OTDR | Locate faults, measure loss |
| VFL | Visual fault locator (red light) |
| Inspection Scope | Check connector end face |

---

*Previous: [← SONET/SDH](./sonet-sdh.md) | Next: [Ethernet →](./ethernet.md)*

