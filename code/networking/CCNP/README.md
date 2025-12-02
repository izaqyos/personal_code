# CCNP Enterprise Study Guide 🎓

> **Advanced networking for experienced professionals - Post-CCNA pathway**

## 📋 Overview

This project continues from the [CCNA Refresher](../CCNA/) and covers CCNP Enterprise level material. The CCNP Enterprise certification demonstrates your ability to plan, implement, verify, and troubleshoot enterprise network solutions.

### CCNP Enterprise Certification Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CCNP Enterprise                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   REQUIRED: Core Exam                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  350-401 ENCOR                                                      │  │
│   │  Implementing Cisco Enterprise Network Core Technologies            │  │
│   │  Duration: 120 min | Questions: 90-110                              │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   PLUS ONE: Concentration Exam (choose one)                                │
│   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ │
│   │ 300-410       │ │ 300-415       │ │ 300-420       │ │ 300-425       │ │
│   │ ENARSI        │ │ ENSDWI        │ │ ENSLD         │ │ ENWLSD        │ │
│   │ Adv Routing   │ │ SD-WAN        │ │ Design        │ │ Wireless      │ │
│   └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Prerequisites

- ✅ CCNA certification (or equivalent knowledge)
- ✅ Complete [CCNA Refresher](../CCNA/) first
- ✅ 3-5 years networking experience recommended

## 🗂️ Project Structure

```
CCNP/
├── README.md                    # This file
├── ROADMAP.md                   # Learning path & time estimates
├── PROGRESS.md                  # Track your progress (pause/resume)
│
├── modules/
│   ├── 01-architecture/         # Enterprise design, SD-Access, SD-WAN
│   ├── 02-virtualization/       # VRF, GRE, IPsec, LISP, VXLAN
│   ├── 03-infrastructure/       # EIGRP, OSPF, BGP, Multicast
│   ├── 04-network-assurance/    # Monitoring, troubleshooting, analytics
│   ├── 05-security/             # Advanced ACLs, CoPP, 802.1X, MACsec
│   └── 06-automation/           # Python, APIs, Ansible, DNA Center
│
├── exercises/
│   ├── eve-ng-labs/             # Advanced labs (EVE-NG/GNS3)
│   └── troubleshooting/         # Complex scenarios
│
├── cheatsheets/                 # Quick reference cards
└── practice-exams/              # Self-assessment
```

## 🆚 CCNA vs CCNP Comparison

| Topic | CCNA Level | CCNP Level |
|-------|------------|------------|
| OSPF | Single/Multi-area basics | LSA types, filtering, summarization, troubleshooting |
| BGP | Not covered | Full eBGP/iBGP, path attributes, route policies |
| EIGRP | Not covered | Full configuration, optimization, troubleshooting |
| Switching | VLANs, STP basics | MST, advanced STP tuning, Layer 3 switching |
| Security | Basic ACLs, port security | CoPP, uRPF, 802.1X, MACsec, DMVPN |
| Wireless | WLC concepts | Advanced RF, roaming, design, troubleshooting |
| Automation | API basics | Python scripting, NETCONF, RESTCONF, Ansible |
| SD-WAN | Concepts | Full implementation (vManage, vBond, vSmart, vEdge) |
| SD-Access | Concepts | Fabric design, underlay/overlay, ISE integration |

## 📊 ENCOR Exam Domains

```
┌──────────────────────────────────────────────────────────────────┐
│                    350-401 ENCOR Exam Weight                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Architecture              ███████████████ 15%                   │
│  Virtualization            ██████████████████████ 20%            │
│  Infrastructure            ██████████████████████████████ 30%    │
│  Network Assurance         ██████████████ 10%                    │
│  Security                  ██████████████████████ 20%            │
│  Automation                █████████ 10%                         │ 
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 🚀 Getting Started

### Recommended Study Order

1. **Architecture** (15%) - Enterprise design principles
2. **Infrastructure** (30%) - Core routing/switching (heaviest topic!)
3. **Virtualization** (20%) - Overlay technologies
4. **Security** (20%) - Advanced protection
5. **Network Assurance** (10%) - Monitoring & analytics
6. **Automation** (10%) - Programming skills

### Study Timeline

| Experience Level | Daily Study | Est. Completion |
|------------------|-------------|-----------------|
| Strong CCNA + Experience | 2 hours | 4-6 months |
| Average CCNA | 2-3 hours | 6-9 months |
| Need CCNA Review | 3-4 hours | 9-12 months |

## 🛠️ Lab Requirements

CCNP labs are more complex and require better tools:

### Recommended Lab Platforms

| Platform | Type | Pros | Cons |
|----------|------|------|------|
| EVE-NG | Local VM | Full Cisco IOS support | Requires images |
| GNS3 | Local | Good for routing labs | Complex setup |
| Cisco CML | Official | Full support, legal | $199/year personal |
| Cisco DevNet | Cloud | Free sandboxes | Limited time |

### Minimum Lab Specs
- **RAM**: 32GB recommended (16GB minimum)
- **CPU**: 8+ cores
- **Storage**: 100GB+ SSD
- **Cisco images**: IOSv, IOSvL2, CSR1000v, vWLC

## 📚 Recommended Resources

### Books
- *CCNP ENCOR 350-401 Official Cert Guide* - Kevin Wallace
- *CCNP Enterprise Advanced Routing ENARSI* - Brad Edgeworth
- *Routing TCP/IP Volume I & II* - Jeff Doyle (deep dive)

### Video Courses
- INE - CCNP Enterprise
- CBT Nuggets - CCNP Enterprise
- Cisco U. - Official training

### Practice
- Boson ExSim - Practice exams
- Cisco Learning Labs
- EVE-NG Community Labs

## ⚡ Quick Start

```bash
# Navigate to CCNP project
cd /Users/yosii/work/git/personal_code/code/networking/CCNP

# Check your progress
cat PROGRESS.md

# Start with Module 1
cd modules/01-architecture
```

---

**Good luck on your CCNP journey!** 🎯

*Last updated: December 2025*

