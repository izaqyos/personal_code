# CCNA Refresher Roadmap 🗺️

> **Estimated total time: 40-60 hours** (adjustable based on prior knowledge)

## Learning Path Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  WEEK 1-2          WEEK 3-4          WEEK 5-6          WEEK 7-8            │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐       ┌─────────┐         │
│  │ Module  │       │ Module  │       │ Module  │       │ Module  │         │
│  │   1     │──────▶│   2     │──────▶│   3     │──────▶│   4     │         │
│  │Network  │       │Network  │       │  IP     │       │  IP     │         │
│  │Fundmntl │       │ Access  │       │Connect. │       │Services │         │
│  └─────────┘       └─────────┘       └─────────┘       └─────────┘         │
│       │                 │                 │                 │               │
│       ▼                 ▼                 ▼                 ▼               │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐       ┌─────────┐         │
│  │  Labs   │       │  Labs   │       │  Labs   │       │  Labs   │         │
│  └─────────┘       └─────────┘       └─────────┘       └─────────┘         │
│                                                                             │
│  WEEK 9-10         WEEK 11-12        WEEK 13+                              │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐                           │
│  │ Module  │       │ Module  │       │Practice │                           │
│  │   5     │──────▶│   6     │──────▶│ Exams & │                           │
│  │Security │       │Automate │       │ Review  │                           │
│  │         │       │  🆕     │       │         │                           │
│  └─────────┘       └─────────┘       └─────────┘                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Module 1: Network Fundamentals (20% of exam)
**⏱️ Estimated Time: 6-8 hours | 🔄 Refresh Level: Medium**

### Topics

| # | Topic | Status | Time | Priority |
|---|-------|--------|------|----------|
| 1.1 | OSI & TCP/IP Models Review | ⬜ | 30 min | 🟢 Quick |
| 1.2 | Network Components & Topologies | ⬜ | 45 min | 🟢 Quick |
| 1.3 | IPv4 Addressing & Subnetting | ⬜ | 90 min | 🟡 Review |
| 1.4 | IPv6 Addressing (expanded) | ⬜ | 90 min | 🔴 Focus |
| 1.5 | TCP vs UDP Deep Dive | ⬜ | 30 min | 🟢 Quick |
| 1.6 | Network Cabling & Speeds | ⬜ | 30 min | 🟡 Review |
| 1.7 | Wireless Fundamentals | ⬜ | 60 min | 🔴 Focus |
| 1.8 | Virtualization Concepts | ⬜ | 45 min | 🔴 NEW |

### Key Changes Since Your Last CCNA
- **IPv6 is now mandatory** - Equal weight to IPv4
- **Wireless fundamentals** - Now part of core CCNA
- **Virtualization** - VMs, containers, cloud concepts

---

## Module 2: Network Access (20% of exam)
**⏱️ Estimated Time: 8-10 hours | 🔄 Refresh Level: Medium**

### Topics

| # | Topic | Status | Time | Priority |
|---|-------|--------|------|----------|
| 2.1 | VLANs & Trunking | ⬜ | 90 min | 🟡 Review |
| 2.2 | Inter-VLAN Routing | ⬜ | 60 min | 🟡 Review |
| 2.3 | STP/RSTP/PVST+ | ⬜ | 90 min | 🟡 Review |
| 2.4 | EtherChannel (LACP/PAgP) | ⬜ | 60 min | 🟡 Review |
| 2.5 | Wireless Architectures | ⬜ | 60 min | 🔴 NEW |
| 2.6 | AP Modes & WLC | ⬜ | 60 min | 🔴 NEW |
| 2.7 | Physical Layer Concepts | ⬜ | 30 min | 🟢 Quick |

### Key Changes Since Your Last CCNA
- **Wireless LAN Controllers (WLC)** - Centralized management
- **Lightweight vs Autonomous APs** - New architecture
- **802.11ax (Wi-Fi 6)** - Latest standard

---

## Module 3: IP Connectivity (25% of exam)
**⏱️ Estimated Time: 10-12 hours | 🔄 Refresh Level: High**

### Topics

| # | Topic | Status | Time | Priority |
|---|-------|--------|------|----------|
| 3.1 | Static Routing | ⬜ | 60 min | 🟢 Quick |
| 3.2 | Dynamic Routing Concepts | ⬜ | 45 min | 🟡 Review |
| 3.3 | OSPF Single-Area | ⬜ | 120 min | 🟡 Review |
| 3.4 | OSPF Multi-Area | ⬜ | 90 min | 🟡 Review |
| 3.5 | OSPF Troubleshooting | ⬜ | 60 min | 🟡 Review |
| 3.6 | First Hop Redundancy (HSRP) | ⬜ | 60 min | 🟡 Review |
| 3.7 | IPv6 Routing | ⬜ | 90 min | 🔴 Focus |

### Key Changes Since Your Last CCNA
- **EIGRP removed** - Now CCNP only
- **RIP removed** - Legacy protocol
- **OSPF is primary focus** - Single and multi-area
- **IPv6 routing** - OSPFv3, static IPv6 routes

---

## Module 4: IP Services (10% of exam)
**⏱️ Estimated Time: 6-8 hours | 🔄 Refresh Level: Medium**

### Topics

| # | Topic | Status | Time | Priority |
|---|-------|--------|------|----------|
| 4.1 | NAT/PAT Configuration | ⬜ | 60 min | 🟡 Review |
| 4.2 | DHCP (v4 and v6) | ⬜ | 60 min | 🟡 Review |
| 4.3 | DNS Fundamentals | ⬜ | 30 min | 🟢 Quick |
| 4.4 | NTP Configuration | ⬜ | 30 min | 🟢 Quick |
| 4.5 | SNMP & Syslog | ⬜ | 45 min | 🟡 Review |
| 4.6 | QoS Concepts | ⬜ | 60 min | 🔴 NEW |
| 4.7 | SSH & Remote Access | ⬜ | 30 min | 🟢 Quick |

### Key Changes Since Your Last CCNA
- **DHCPv6** - Stateful and stateless
- **QoS concepts** - Classification, marking, queuing
- **SNMP versions** - v2c and v3 security

---

## Module 5: Security Fundamentals (15% of exam)
**⏱️ Estimated Time: 6-8 hours | 🔄 Refresh Level: High**

### Topics

| # | Topic | Status | Time | Priority |
|---|-------|--------|------|----------|
| 5.1 | Security Concepts & Threats | ⬜ | 45 min | 🔴 Focus |
| 5.2 | Access Control Lists (ACLs) | ⬜ | 90 min | 🟡 Review |
| 5.3 | Layer 2 Security | ⬜ | 60 min | 🔴 Focus |
| 5.4 | AAA Concepts | ⬜ | 45 min | 🟡 Review |
| 5.5 | Wireless Security | ⬜ | 60 min | 🔴 NEW |
| 5.6 | VPN Fundamentals | ⬜ | 45 min | 🔴 NEW |
| 5.7 | Device Hardening | ⬜ | 30 min | 🟡 Review |

### Key Changes Since Your Last CCNA
- **Layer 2 attacks** - DHCP snooping, DAI, port security
- **Wireless security** - WPA3, 802.1X
- **VPN concepts** - Site-to-site, remote access
- **Zero Trust** - Modern security model

---

## Module 6: Automation & Programmability (10% of exam) 🆕
**⏱️ Estimated Time: 8-10 hours | 🔄 Refresh Level: NEW MATERIAL**

### Topics

| # | Topic | Status | Time | Priority |
|---|-------|--------|------|----------|
| 6.1 | Network Automation Benefits | ⬜ | 30 min | 🔴 NEW |
| 6.2 | REST APIs & HTTP | ⬜ | 60 min | 🔴 NEW |
| 6.3 | JSON & YAML Data Formats | ⬜ | 45 min | 🔴 NEW |
| 6.4 | Configuration Management | ⬜ | 60 min | 🔴 NEW |
| 6.5 | SDN & Controllers | ⬜ | 60 min | 🔴 NEW |
| 6.6 | Cisco DNA Center | ⬜ | 60 min | 🔴 NEW |
| 6.7 | Python for Networking | ⬜ | 90 min | 🔴 NEW |

### This Module is Completely New!
- **API-driven management** - REST, RESTCONF, NETCONF
- **Data serialization** - JSON, YAML, XML
- **Configuration tools** - Ansible, Puppet, Chef
- **SDN architectures** - Controller-based networking
- **Cisco DNA Center** - Intent-based networking
- **Python basics** - Scripts for network automation

---

## Exam Breakdown Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                    CCNA 200-301 Exam Weight                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Network Fundamentals     ████████████████████ 20%               │
│  Network Access           ████████████████████ 20%               │
│  IP Connectivity          █████████████████████████ 25%          │
│  IP Services              ██████████ 10%                         │
│  Security Fundamentals    ███████████████ 15%                    │
│  Automation/Programmable  ██████████ 10%  🆕                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Recommended Study Order

### Phase 1: Foundation Refresh (Weeks 1-4)
1. Module 1: Network Fundamentals
2. Module 2: Network Access
   - Focus on VLANs, STP, wireless basics

### Phase 2: Core Skills (Weeks 5-8)
3. Module 3: IP Connectivity
   - Heavy focus on OSPF
4. Module 4: IP Services
   - NAT, DHCP, DNS, NTP

### Phase 3: Modern Skills (Weeks 9-12)
5. Module 5: Security
   - Layer 2 security, ACLs, wireless security
6. Module 6: Automation 🆕
   - APIs, JSON, Python basics

### Phase 4: Review & Practice (Weeks 13+)
7. Practice exams
8. Lab exercises
9. Weak area review

---

## Priority Legend

| Symbol | Meaning | Action |
|--------|---------|--------|
| 🟢 Quick | You know this | Skim & verify |
| 🟡 Review | Needs refresh | Read & practice |
| 🔴 Focus | New/changed | Deep study |
| 🆕 NEW | Didn't exist before | Learn from scratch |

---

*Continue to [PROGRESS.md](./PROGRESS.md) to track your learning journey*

