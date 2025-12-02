# Module 2: Network Access 🔌

> **20% of CCNA Exam | Estimated Time: 8-10 hours**

## Module Overview

This module covers Layer 2 technologies - switching, VLANs, and spanning tree. Much of this will be familiar, but wireless architectures are new to the CCNA curriculum.

---

## Table of Contents

1. [VLANs & Trunking](#1-vlans--trunking)
2. [Inter-VLAN Routing](#2-inter-vlan-routing)
3. [Spanning Tree Protocol](#3-spanning-tree-protocol)
4. [EtherChannel](#4-etherchannel)
5. [Wireless Architectures](#5-wireless-architectures)
6. [AP Modes & WLC](#6-ap-modes--wlc)

---

## 1. VLANs & Trunking

### VLAN Concepts

```
Without VLANs:                    With VLANs:
┌─────────────────────┐          ┌─────────────────────┐
│    One Broadcast    │          │ VLAN10 │ VLAN20    │
│       Domain        │          │  Sales │ Engineer  │
│  PC  PC  PC  PC     │          │ PC PC  │  PC  PC   │
└─────────────────────┘          └────────┴───────────┘
All traffic flooded               Isolated broadcast domains
```

### VLAN Types

| VLAN Type | Purpose |
|-----------|---------|
| Data VLAN | User traffic |
| Voice VLAN | VoIP traffic (QoS tagged) |
| Management VLAN | Switch management traffic |
| Native VLAN | Untagged traffic on trunk |
| Default VLAN | VLAN 1 (avoid using) |

### VLAN Configuration

```cisco
! Create VLANs
Switch(config)# vlan 10
Switch(config-vlan)# name SALES
Switch(config-vlan)# exit
Switch(config)# vlan 20
Switch(config-vlan)# name ENGINEERING

! Assign ports to VLANs (Access mode)
Switch(config)# interface range fa0/1-10
Switch(config-if-range)# switchport mode access
Switch(config-if-range)# switchport access vlan 10

! Configure Voice VLAN
Switch(config)# interface fa0/11
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config-if)# switchport voice vlan 50

! Verify
Switch# show vlan brief
Switch# show interfaces fa0/1 switchport
```

### Trunking (802.1Q)

```
┌─────────────┐                    ┌─────────────┐
│  Switch A   │  Trunk (802.1Q)    │  Switch B   │
│  VLAN 10,20 │════════════════════│  VLAN 10,20 │
└─────────────┘  Tagged frames     └─────────────┘
                 carry VLAN ID
```

### 802.1Q Frame Format

```
┌────────────────────────────────────────────────────────────────┐
│ Dest MAC │ Src MAC │ 802.1Q Tag │ Type │ Data │ FCS           │
└────────────────────────────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │ TPID │ PRI │ CFI │ VID │
              │ 0x8100│ 3b │ 1b │ 12b │
              └─────────────────────┘
              VLAN ID: 1-4094
```

### Trunk Configuration

```cisco
! Configure trunk port
Switch(config)# interface gi0/1
Switch(config-if)# switchport trunk encapsulation dot1q
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk native vlan 99
Switch(config-if)# switchport trunk allowed vlan 10,20,30

! Verify
Switch# show interfaces trunk
Switch# show interfaces gi0/1 switchport
```

### DTP (Dynamic Trunking Protocol)

| Mode | Description | Recommendation |
|------|-------------|----------------|
| access | Always access, no DTP | Use for end devices |
| trunk | Always trunk, sends DTP | Use for switch links |
| dynamic auto | Trunk if neighbor asks | Avoid |
| dynamic desirable | Actively tries to trunk | Avoid |

**Best Practice**: Disable DTP on all ports

```cisco
Switch(config-if)# switchport nonegotiate
```

---

## 2. Inter-VLAN Routing

### Method 1: Router-on-a-Stick

```
                    ┌─────────────┐
                    │   Router    │
                    │  Gi0/0.10   │ (subinterfaces)
                    │  Gi0/0.20   │
                    └──────┬──────┘
                           │ Trunk
                    ┌──────┴──────┐
                    │   Switch    │
                    │ VLAN10 VLAN20│
                    └─────────────┘
```

```cisco
! Router Configuration
Router(config)# interface gi0/0
Router(config-if)# no shutdown

Router(config)# interface gi0/0.10
Router(config-subif)# encapsulation dot1q 10
Router(config-subif)# ip address 192.168.10.1 255.255.255.0

Router(config)# interface gi0/0.20
Router(config-subif)# encapsulation dot1q 20
Router(config-subif)# ip address 192.168.20.1 255.255.255.0
```

### Method 2: Layer 3 Switch (SVI)

```
                    ┌─────────────┐
                    │   L3 Switch │
                    │  VLAN10 SVI │ (Switched Virtual Interfaces)
                    │  VLAN20 SVI │
                    │ VLAN10 VLAN20│
                    └─────────────┘
```

```cisco
! L3 Switch Configuration
Switch(config)# ip routing

Switch(config)# interface vlan 10
Switch(config-if)# ip address 192.168.10.1 255.255.255.0
Switch(config-if)# no shutdown

Switch(config)# interface vlan 20
Switch(config-if)# ip address 192.168.20.1 255.255.255.0
Switch(config-if)# no shutdown

! Verify
Switch# show ip route
Switch# show interfaces vlan 10
```

### Comparison

| Feature | Router-on-a-Stick | L3 Switch |
|---------|-------------------|-----------|
| Cost | Lower | Higher |
| Performance | Limited by single link | Hardware-based |
| Scalability | Poor | Excellent |
| Use Case | Small networks | Enterprise |

---

## 3. Spanning Tree Protocol

### Why STP?

```
Without STP (Broadcast Storm):
┌────────┐        ┌────────┐
│   SW1  │════════│  SW2   │
└───┬────┘        └────┬───┘
    │                  │
    │    ┌────────┐    │
    └════│  SW3   │════┘
         └────────┘
         
Frames loop forever!
```

### STP Versions

| Protocol | Standard | Convergence | Features |
|----------|----------|-------------|----------|
| STP | 802.1D | 30-50 sec | Original, slow |
| RSTP | 802.1w | <10 sec | Rapid convergence |
| PVST+ | Cisco | 30-50 sec per VLAN | Per-VLAN STP |
| Rapid PVST+ | Cisco | <10 sec per VLAN | **Recommended** |
| MST | 802.1s | <10 sec | Multiple VLANs per instance |

### STP Operation

```
1. Elect Root Bridge (lowest Bridge ID)
   Bridge ID = Priority (default 32768) + VLAN + MAC Address

2. Calculate Root Path Cost
   ┌──────────────────────────────────────┐
   │ Speed      │ STP Cost │ RSTP Cost   │
   ├──────────────────────────────────────┤
   │ 10 Mbps    │   100    │  2,000,000  │
   │ 100 Mbps   │    19    │    200,000  │
   │ 1 Gbps     │     4    │     20,000  │
   │ 10 Gbps    │     2    │      2,000  │
   └──────────────────────────────────────┘

3. Determine Port Roles
   - Root Port (RP): Best path to root (non-root switches)
   - Designated Port (DP): Best port on segment
   - Blocked/Alternate: Redundant paths blocked
```

### STP Port States

```
STP (802.1D):                RSTP (802.1w):
Disabled ───┐               Discarding (combines 3)
Blocking ───┼── 20 sec ──▶  Discarding
Listening ──┤                    │
            └── 15 sec ──▶  Learning ─── 15 sec ──▶ Forwarding
                                                         │
                                               (traffic flows)
```

### STP Configuration

```cisco
! Set switch as root bridge
Switch(config)# spanning-tree vlan 10 root primary
! OR manually set priority
Switch(config)# spanning-tree vlan 10 priority 4096

! Enable Rapid PVST+ (recommended)
Switch(config)# spanning-tree mode rapid-pvst

! Configure PortFast (access ports only!)
Switch(config)# interface range fa0/1-24
Switch(config-if-range)# spanning-tree portfast
Switch(config-if-range)# spanning-tree bpduguard enable

! Global PortFast for all access ports
Switch(config)# spanning-tree portfast default

! Verify
Switch# show spanning-tree
Switch# show spanning-tree vlan 10
Switch# show spanning-tree interface fa0/1
```

### STP Protection Features

| Feature | Purpose | Configuration |
|---------|---------|---------------|
| PortFast | Skip listening/learning | Access ports only |
| BPDU Guard | Disable port if BPDU received | With PortFast |
| Root Guard | Prevent unauthorized root | On designated ports |
| Loop Guard | Prevent unidirectional links | On non-designated ports |

---

## 4. EtherChannel

### What is EtherChannel?

```
Without EtherChannel:          With EtherChannel:
┌────────┐      ┌────────┐    ┌────────┐        ┌────────┐
│  SW1   │──────│  SW2   │    │  SW1   │════════│  SW2   │
│        │──────│        │    │        │ Po1    │        │
│        │──────│        │    │        │(3 Gbps)│        │
└────────┘      └────────┘    └────────┘        └────────┘
STP blocks 2 links!           All links active, one logical
```

### EtherChannel Protocols

| Protocol | Standard | Negotiation |
|----------|----------|-------------|
| LACP | 802.3ad (IEEE) | Active/Passive |
| PAgP | Cisco proprietary | Desirable/Auto |
| Static | None | On (no negotiation) |

### LACP Configuration

```cisco
! Configure LACP EtherChannel
Switch(config)# interface range gi0/1-2
Switch(config-if-range)# channel-group 1 mode active
Switch(config-if-range)# exit

! Configure the Port-channel interface
Switch(config)# interface port-channel 1
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20,30

! Verify
Switch# show etherchannel summary
Switch# show etherchannel port-channel
Switch# show interfaces port-channel 1
```

### LACP Modes

| Mode | Behavior |
|------|----------|
| Active | Actively negotiates LACP |
| Passive | Responds to LACP only |

```
Active  ←→ Active   = EtherChannel forms
Active  ←→ Passive  = EtherChannel forms
Passive ←→ Passive  = No EtherChannel!
```

### Load Balancing

```cisco
! View current load balancing
Switch# show etherchannel load-balance

! Change load balancing method
Switch(config)# port-channel load-balance src-dst-ip
```

| Method | Description |
|--------|-------------|
| src-mac | Source MAC |
| dst-mac | Destination MAC |
| src-dst-mac | Both MAC addresses |
| src-ip | Source IP |
| dst-ip | Destination IP |
| src-dst-ip | Both IP addresses |

---

## 5. Wireless Architectures 🔴 NEW TOPIC

### Wireless Deployment Models

```
1. Autonomous AP (Standalone)
┌──────────┐     ┌──────────┐
│    AP    │     │    AP    │  Each AP configured individually
│ (config) │     │ (config) │  No central management
└──────────┘     └──────────┘

2. Lightweight AP + WLC (Centralized)
┌──────────┐     ┌──────────┐
│ Lightwt  │═════│   WLC    │  AP is "dumb"
│    AP    │     │ (config) │  WLC manages all APs
└──────────┘     └──────────┘
    CAPWAP tunnel

3. Cloud-based (Cisco Meraki)
┌──────────┐     ┌──────────┐
│    AP    │─────│  Cloud   │  Config in cloud dashboard
└──────────┘     │Controller│  Internet-dependent
                 └──────────┘

4. FlexConnect (Hybrid)
┌──────────┐     ┌──────────┐
│ FlexConn │═════│   WLC    │  Local switching capability
│    AP    │     │(Central) │  Works if WLC unreachable
└──────────┘     └──────────┘
```

### CAPWAP (Control And Provisioning of Wireless APs)

```
┌─────────────────────────────────────────────────────────────┐
│                      CAPWAP Operation                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Control Messages (UDP 5246)    Data Traffic (UDP 5247)    │
│  ─────────────────────────      ─────────────────────────  │
│  • AP configuration             • User data (encrypted)    │
│  • Firmware updates             • Tunneled to WLC          │
│  • Client authentication        • OR local switching       │
│                                                             │
│  ┌──────┐         CAPWAP Tunnel          ┌──────┐          │
│  │  AP  │═══════════════════════════════│ WLC  │          │
│  └──────┘   Control + Data (default)    └──────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Split-MAC Architecture

| Function | Autonomous AP | Lightweight AP | WLC |
|----------|---------------|----------------|-----|
| Beacons | ✓ | ✓ | |
| Probes | ✓ | ✓ | |
| RF management | ✓ | | ✓ |
| Authentication | ✓ | | ✓ |
| Association | ✓ | | ✓ |
| Frame encryption | ✓ | ✓ | |
| QoS | ✓ | | ✓ |

---

## 6. AP Modes & WLC

### AP Operating Modes

| Mode | Purpose |
|------|---------|
| Local | Normal operation, serves clients |
| FlexConnect | Local switching when WLC unavailable |
| Monitor | Dedicated scanning (no client service) |
| Rogue Detector | Detects unauthorized APs |
| Sniffer | Captures packets for analysis |
| Bridge | Point-to-point/multipoint bridging |
| SE-Connect | Spectrum analysis |

### WLC Ports and Interfaces

```
Physical Ports:
┌─────────────────────────────────────────────────────────────┐
│ Service Port │ Distribution Ports │ Console │ Redundancy   │
│  (mgmt OOB)  │   (trunk links)    │         │              │
└─────────────────────────────────────────────────────────────┘

Logical Interfaces:
┌─────────────────────────────────────────────────────────────┐
│ Management │ AP-Manager │ Virtual │ Service │ Dynamic      │
│ Interface  │ Interface  │Interface│ Port    │ Interface    │
│            │            │         │ Interface│ (per WLAN)   │
└─────────────────────────────────────────────────────────────┘
```

### WLC Interface Types

| Interface | Purpose |
|-----------|---------|
| Management | In-band management (SSH, HTTPS, SNMP) |
| AP-Manager | AP communication (CAPWAP) |
| Virtual | DHCP relay, web auth, mobility |
| Service Port | Out-of-band management |
| Dynamic | Maps WLANs to VLANs |

### Wireless Security Methods

```
┌─────────────────────────────────────────────────────────────┐
│                   Wireless Security                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Personal (PSK)              Enterprise (802.1X)           │
│  ───────────────             ─────────────────────          │
│  • Pre-shared key            • RADIUS server               │
│  • Same key for all          • Individual credentials      │
│  • Home/small office         • Corporate environment       │
│                                                             │
│  WPA2-Personal               WPA2-Enterprise               │
│  ┌────────┐                  ┌────────┐    ┌────────┐      │
│  │ Client │──PSK────────────▶│   AP   │───▶│ RADIUS │      │
│  └────────┘                  └────────┘    └────────┘      │
│                                                             │
│  WPA3-Personal               WPA3-Enterprise               │
│  • SAE (more secure)         • 192-bit security mode       │
│  • Protection against        • Stronger encryption         │
│    offline attacks                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Module 2 Exercises

### Exercise 2.1: VLAN Configuration
Create the following VLAN setup:
- VLAN 10: Sales (ports 1-8)
- VLAN 20: Engineering (ports 9-16)
- VLAN 30: Management (ports 17-20)
- VLAN 99: Native (trunk only)
- Voice VLAN 50 on all access ports

### Exercise 2.2: STP Root Bridge
Given three switches with these MAC addresses:
- SW1: 0000.0000.0001, priority 32768
- SW2: 0000.0000.0002, priority 32768
- SW3: 0000.0000.0003, priority 32768

1. Which switch is root?
2. What priority would SW3 need to become root?
3. Configure SW3 as root bridge

### Exercise 2.3: EtherChannel
Configure LACP EtherChannel between two switches:
- Use interfaces Gi0/1 and Gi0/2
- Create Port-channel 1
- Configure as trunk with VLANs 10, 20, 30

### Exercise 2.4: Wireless Concepts
Match the wireless component:
1. CAPWAP → ___
2. WLC → ___
3. FlexConnect → ___
4. 802.1X → ___

---

## 🔗 Additional Resources

- [Cisco VLAN Configuration Guide](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/16-12/configuration_guide/vlan/b_1612_vlan_9300_cg.html)
- [STP Toolkit](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24062-146.html)
- [Wireless Design Guide](https://www.cisco.com/c/en/us/solutions/enterprise-networks/802-11ax-solution/wireless-702-deployment-guide.html)

---

*Previous: [← Network Fundamentals](../01-network-fundamentals/README.md) | Next: [IP Connectivity →](../03-ip-connectivity/README.md)*

