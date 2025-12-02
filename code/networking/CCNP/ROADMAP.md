# CCNP Enterprise Roadmap 🗺️

> **Estimated total time: 200-400 hours** (depending on experience)

## Learning Path Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  MONTH 1-2           MONTH 3-4           MONTH 5-6           MONTH 7+      │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐         ┌─────────┐   │
│  │ Module  │         │ Module  │         │ Module  │         │ Module  │   │
│  │  1 & 2  │────────▶│    3    │────────▶│  4 & 5  │────────▶│    6    │   │
│  │Arch+Virt│         │ Infra   │         │Assur+Sec│         │ Automat │   │
│  └─────────┘         └─────────┘         └─────────┘         └─────────┘   │
│                                                                   │         │
│                                                                   ▼         │
│                                                            ┌─────────┐     │
│                                                            │  ENCOR  │     │
│                                                            │  EXAM   │     │
│                                                            └─────────┘     │
│                                                                   │         │
│                                                                   ▼         │
│                                                            ┌─────────┐     │
│                                                            │ Concen- │     │
│                                                            │ tration │     │
│                                                            │  Exam   │     │
│                                                            └─────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Module 1: Architecture (15% of exam)
**⏱️ Estimated Time: 25-35 hours**

### Topics

| # | Topic | Status | Time | From CCNA |
|---|-------|--------|------|-----------|
| 1.1 | Enterprise Network Design | ⬜ | 3 hr | New depth |
| 1.2 | High Availability Concepts | ⬜ | 3 hr | Expanded |
| 1.3 | SD-Access Architecture | ⬜ | 5 hr | 🆕 NEW |
| 1.4 | SD-WAN Architecture | ⬜ | 5 hr | 🆕 NEW |
| 1.5 | QoS Architecture | ⬜ | 4 hr | Expanded |
| 1.6 | Hardware & Switching Platforms | ⬜ | 3 hr | New depth |
| 1.7 | Wireless Design Principles | ⬜ | 4 hr | Expanded |

### Key Concepts

```
Enterprise Design:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Traditional              │  Software-Defined              │
│  ───────────────          │  ─────────────────             │
│  Three-Tier/Two-Tier      │  SD-Access (Campus)           │
│  Collapsed Core           │  SD-WAN (WAN)                 │
│  VSS/StackWise            │  ACI (Data Center)            │
│                           │  DNA Center (Management)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Module 2: Virtualization (20% of exam)
**⏱️ Estimated Time: 40-50 hours**

### Topics

| # | Topic | Status | Time | From CCNA |
|---|-------|--------|------|-----------|
| 2.1 | VRF & VRF-Lite | ⬜ | 5 hr | 🆕 NEW |
| 2.2 | GRE Tunnels | ⬜ | 4 hr | Concepts only |
| 2.3 | IPsec VPN (Site-to-Site) | ⬜ | 6 hr | Concepts only |
| 2.4 | DMVPN | ⬜ | 8 hr | 🆕 NEW |
| 2.5 | LISP | ⬜ | 6 hr | 🆕 NEW |
| 2.6 | VXLAN | ⬜ | 6 hr | 🆕 NEW |
| 2.7 | Network Virtualization | ⬜ | 4 hr | Expanded |

### Key Technologies

```
Overlay Technologies:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Technology    │  Use Case           │  Encapsulation      │
│  ────────────────────────────────────────────────────────   │
│  GRE           │  Basic tunneling    │  IP Protocol 47     │
│  IPsec         │  Secure tunnels     │  ESP/AH             │
│  DMVPN         │  Dynamic mesh VPN   │  GRE + NHRP         │
│  LISP          │  Mobility/SD-Access │  UDP 4341/4342      │
│  VXLAN         │  Data center        │  UDP 4789           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Module 3: Infrastructure (30% of exam) ⚠️ HEAVIEST
**⏱️ Estimated Time: 60-80 hours**

### Topics

| # | Topic | Status | Time | From CCNA |
|---|-------|--------|------|-----------|
| 3.1 | EIGRP | ⬜ | 10 hr | 🆕 NEW (was removed from CCNA) |
| 3.2 | OSPF Advanced | ⬜ | 10 hr | Deep expansion |
| 3.3 | BGP | ⬜ | 15 hr | 🆕 NEW |
| 3.4 | Route Redistribution | ⬜ | 8 hr | 🆕 NEW |
| 3.5 | Route Filtering & Manipulation | ⬜ | 8 hr | 🆕 NEW |
| 3.6 | Multicast | ⬜ | 8 hr | 🆕 NEW |
| 3.7 | Switching Deep Dive | ⬜ | 6 hr | Expanded |
| 3.8 | Wireless Infrastructure | ⬜ | 6 hr | Expanded |

### Routing Protocol Comparison

```
┌─────────────────────────────────────────────────────────────────────────┐
│              CCNP Routing Protocols Comparison                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Protocol │ Type      │ Metric            │ AD  │ Algorithm            │
│  ─────────────────────────────────────────────────────────────────────  │
│  EIGRP    │ Hybrid    │ Bandwidth+Delay   │ 90  │ DUAL                 │
│  OSPF     │ Link-State│ Cost (BW)         │ 110 │ Dijkstra SPF         │
│  BGP      │ Path-Vec  │ Path Attributes   │ 20/200│ Best Path Selection│
│                                                                         │
│  BGP Path Selection (in order):                                        │
│  1. Highest Weight (Cisco)                                             │
│  2. Highest Local Preference                                           │
│  3. Locally originated                                                 │
│  4. Shortest AS-Path                                                   │
│  5. Lowest Origin type (i > e > ?)                                     │
│  6. Lowest MED                                                         │
│  7. eBGP over iBGP                                                     │
│  8. Lowest IGP metric to next-hop                                      │
│  9. Oldest route                                                       │
│  10. Lowest Router ID                                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Module 4: Network Assurance (10% of exam)
**⏱️ Estimated Time: 20-30 hours**

### Topics

| # | Topic | Status | Time | From CCNA |
|---|-------|--------|------|-----------|
| 4.1 | Network Management Protocols | ⬜ | 4 hr | Expanded |
| 4.2 | DNA Center Assurance | ⬜ | 5 hr | 🆕 NEW |
| 4.3 | NetFlow/IPFIX | ⬜ | 4 hr | 🆕 NEW |
| 4.4 | SPAN/RSPAN/ERSPAN | ⬜ | 3 hr | 🆕 NEW |
| 4.5 | IP SLA | ⬜ | 4 hr | 🆕 NEW |
| 4.6 | Troubleshooting Methodologies | ⬜ | 5 hr | Expanded |

### Network Visibility Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Network Visibility                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Collection        │  Analysis         │  Action            │
│  ──────────────────────────────────────────────────────    │
│  SNMP              │  DNA Center       │  Automated         │
│  NetFlow           │  Assurance        │  Remediation       │
│  Syslog            │  ThousandEyes     │                    │
│  Streaming Telemetry│ Machine Learning │  Alerts            │
│  SPAN              │  Baselines        │  Reports           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Module 5: Security (20% of exam)
**⏱️ Estimated Time: 40-50 hours**

### Topics

| # | Topic | Status | Time | From CCNA |
|---|-------|--------|------|-----------|
| 5.1 | Device Access Control | ⬜ | 4 hr | Expanded |
| 5.2 | Infrastructure Security | ⬜ | 5 hr | Expanded |
| 5.3 | Control Plane Policing (CoPP) | ⬜ | 5 hr | 🆕 NEW |
| 5.4 | 802.1X & MAB | ⬜ | 6 hr | Expanded |
| 5.5 | MACsec | ⬜ | 4 hr | 🆕 NEW |
| 5.6 | TrustSec / SGT | ⬜ | 6 hr | 🆕 NEW |
| 5.7 | Network Segmentation | ⬜ | 4 hr | 🆕 NEW |
| 5.8 | Wireless Security | ⬜ | 5 hr | Expanded |

### Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Zero Trust Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer           │  Technology                              │
│  ─────────────────────────────────────────────────────────  │
│  Identity        │  802.1X, ISE, MFA                        │
│  Device Trust    │  Posture assessment, MDM                 │
│  Network         │  Segmentation, TrustSec, SGT            │
│  Application     │  Micro-segmentation                      │
│  Data            │  Encryption, DLP                         │
│  Analytics       │  DNA Center, SIEM, threat detection      │
│                                                             │
│  "Never trust, always verify"                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Module 6: Automation (10% of exam)
**⏱️ Estimated Time: 25-35 hours**

### Topics

| # | Topic | Status | Time | From CCNA |
|---|-------|--------|------|-----------|
| 6.1 | Python Deep Dive | ⬜ | 6 hr | Expanded |
| 6.2 | NETCONF/YANG | ⬜ | 5 hr | 🆕 NEW |
| 6.3 | RESTCONF | ⬜ | 4 hr | 🆕 NEW |
| 6.4 | Ansible Advanced | ⬜ | 5 hr | Expanded |
| 6.5 | DNA Center APIs | ⬜ | 4 hr | 🆕 NEW |
| 6.6 | Model-Driven Programmability | ⬜ | 4 hr | 🆕 NEW |
| 6.7 | Embedded Event Manager | ⬜ | 3 hr | 🆕 NEW |

### Automation Stack

```
┌─────────────────────────────────────────────────────────────┐
│              Network Automation Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Orchestration Layer                     │   │
│  │         (DNA Center, NSO, Terraform)                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Configuration Management               │   │
│  │            (Ansible, Puppet, Chef)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌───────────┬───────────┬───────────┬───────────┐        │
│  │ NETCONF   │ RESTCONF  │   SSH     │   SNMP    │        │
│  │ (YANG)    │ (YANG)    │  (CLI)    │           │        │
│  └───────────┴───────────┴───────────┴───────────┘        │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Network Infrastructure                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Concentration Exam Options

After passing ENCOR, choose ONE:

### Option 1: ENARSI (300-410) - Advanced Routing
**Best for**: Network engineers focused on routing/switching
- Advanced EIGRP, OSPF, BGP
- Route redistribution
- MPLS VPNs
- Infrastructure troubleshooting

### Option 2: ENSDWI (300-415) - SD-WAN
**Best for**: WAN specialists, modern network engineers
- Cisco SD-WAN architecture
- vManage, vBond, vSmart, vEdge
- Policies, templates, security

### Option 3: ENWLSD (300-425) - Wireless Design
**Best for**: Wireless specialists
- RF design, site surveys
- High-density wireless
- Location services
- Advanced troubleshooting

### Option 4: ENSLD (300-420) - Network Design
**Best for**: Network architects
- Enterprise design methodologies
- Campus, WAN, Data center
- High availability design

---

## Study Schedule Template

### Weekly Schedule (2 hours/day)

| Day | Activity | Time |
|-----|----------|------|
| Mon | Theory/Reading | 2 hr |
| Tue | Lab Practice | 2 hr |
| Wed | Theory/Reading | 2 hr |
| Thu | Lab Practice | 2 hr |
| Fri | Review/Quiz | 2 hr |
| Sat | Deep Lab | 3 hr |
| Sun | Rest/Light Review | 1 hr |

**Total: ~14 hours/week → 6-7 months to exam ready**

---

## Priority Legend

| Symbol | Meaning | Action |
|--------|---------|--------|
| 🟢 | CCNA Foundation | Quick review |
| 🟡 | Expanded Topic | Deeper study |
| 🔴 | New/Complex | Heavy focus |
| 🆕 | Not in CCNA | Learn from scratch |

---

*Continue to [PROGRESS.md](./PROGRESS.md) to track your journey*

