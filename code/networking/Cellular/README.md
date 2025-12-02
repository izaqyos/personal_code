# Cellular Networks 📱

> **Mobile network technologies from 1G to 5G**

## Evolution

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Cellular Generations                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1G (1980s)      Analog voice                                              │
│  │               AMPS, NMT, TACS                                           │
│  ▼                                                                          │
│  2G (1991)       Digital voice, SMS                                        │
│  │               GSM, CDMA, D-AMPS                                         │
│  ├─ 2.5G         Packet data: GPRS (56-114 kbps)                          │
│  ├─ 2.75G        EDGE (up to 384 kbps)                                    │
│  ▼                                                                          │
│  3G (2001)       Mobile broadband                                          │
│  │               UMTS/WCDMA, CDMA2000                                      │
│  ├─ 3.5G         HSPA (up to 14 Mbps)                                     │
│  ├─ 3.75G        HSPA+ (up to 42 Mbps)                                    │
│  ▼                                                                          │
│  4G (2010)       All-IP, high-speed                                        │
│  │               LTE (up to 150 Mbps)                                      │
│  ├─ 4.5G         LTE-A (up to 1 Gbps)                                     │
│  ▼                                                                          │
│  5G (2019)       IoT, ultra-low latency                                    │
│                  5G NR (up to 20 Gbps)                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Contents

| Topic | File | Description |
|-------|------|-------------|
| GSM | [gsm.md](./gsm.md) | 2G architecture and protocols |
| GPRS/EDGE | [gprs.md](./gprs.md) | 2.5G/2.75G packet data |
| 3G/UMTS | [3g.md](./3g.md) | 3G technologies |
| 4G LTE | [lte.md](./lte.md) | 4G Long Term Evolution |
| 5G | [5g.md](./5g.md) | 5G New Radio |

## Frequency Bands

### Common LTE Bands

| Band | Frequency | Region | Notes |
|------|-----------|--------|-------|
| B1 | 2100 MHz | Global | 3G/LTE |
| B3 | 1800 MHz | EU/APAC | Primary LTE |
| B7 | 2600 MHz | EU | High capacity |
| B20 | 800 MHz | EU | Good coverage |
| B4/66 | 1700/2100 MHz | Americas | AWS |
| B12/17 | 700 MHz | US | Good coverage |

### 5G Bands

| Type | Frequency | Range | Speed |
|------|-----------|-------|-------|
| Low-band | <1 GHz | Wide | Moderate |
| Mid-band | 1-6 GHz | Medium | Fast |
| mmWave | 24-100 GHz | Short | Ultra-fast |

## Key Concepts

### Voice vs Data

```
Circuit-Switched (CS):       Packet-Switched (PS):
├─ Voice calls               ├─ Data services
├─ Dedicated channel         ├─ Shared resources
├─ Guaranteed bandwidth      ├─ Best effort
└─ 2G/3G voice              └─ All data, VoLTE
```

### Identifiers

| ID | Full Name | Purpose |
|----|-----------|---------|
| IMSI | International Mobile Subscriber Identity | Unique subscriber ID (on SIM) |
| IMEI | International Mobile Equipment Identity | Unique device ID |
| MSISDN | Mobile Station ISDN Number | Phone number |
| TMSI | Temporary Mobile Subscriber Identity | Privacy protection |

---

*Related: [Network Fundamentals](../CCNA/modules/01-network-fundamentals/)*

