# Module 3: Infrastructure 🛣️

> **30% of ENCOR Exam | Estimated Time: 60-80 hours** ⚠️ HEAVIEST MODULE

## Module Overview

This is the most critical module covering advanced routing protocols. BGP and EIGRP were not in CCNA, and OSPF goes much deeper here.

---

## Table of Contents

1. [EIGRP](#1-eigrp)
2. [OSPF Advanced](#2-ospf-advanced)
3. [BGP](#3-bgp)
4. [Route Redistribution](#4-route-redistribution)
5. [Route Filtering](#5-route-filtering)
6. [Multicast](#6-multicast)

---

## 1. EIGRP

### EIGRP Overview

```
EIGRP (Enhanced Interior Gateway Routing Protocol):
- Cisco proprietary (now open standard RFC 7868)
- Advanced distance vector / hybrid protocol
- Uses DUAL algorithm for loop-free paths
- Fast convergence, supports unequal-cost load balancing

Metric: Composite of Bandwidth + Delay
(Can include reliability, load, MTU - rarely used)

Default K-values: K1=1, K2=0, K3=1, K4=0, K5=0
Metric = 256 × ((10^7 / min_bandwidth) + cumulative_delay)
```

### EIGRP Terminology

| Term | Description |
|------|-------------|
| Feasible Distance (FD) | Total metric to destination |
| Reported/Advertised Distance (RD) | Neighbor's metric to destination |
| Successor | Best path route |
| Feasible Successor | Backup route (RD < FD of successor) |
| Feasibility Condition | RD < current FD (loop prevention) |

### EIGRP Tables

```
┌─────────────────────────────────────────────────────────────┐
│                      EIGRP Tables                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Neighbor Table:                                            │
│  • Lists adjacent EIGRP neighbors                          │
│  • Holdtime, SRTT, Queue count                             │
│  show ip eigrp neighbors                                    │
│                                                             │
│  Topology Table:                                            │
│  • All routes learned from neighbors                       │
│  • Contains Successors and Feasible Successors             │
│  show ip eigrp topology                                     │
│                                                             │
│  Routing Table:                                             │
│  • Best routes (Successors only)                           │
│  show ip route eigrp                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### EIGRP Configuration

```cisco
! Named EIGRP (preferred)
Router(config)# router eigrp ENTERPRISE
Router(config-router)# address-family ipv4 unicast autonomous-system 100
Router(config-router-af)# network 10.0.0.0 0.255.255.255
Router(config-router-af)# eigrp router-id 1.1.1.1
Router(config-router-af)# af-interface default
Router(config-router-af-interface)# passive-interface
Router(config-router-af-interface)# exit
Router(config-router-af)# af-interface GigabitEthernet0/0
Router(config-router-af-interface)# no passive-interface
Router(config-router-af-interface)# exit

! Classic EIGRP (legacy)
Router(config)# router eigrp 100
Router(config-router)# network 10.0.0.0
Router(config-router)# no auto-summary
Router(config-router)# eigrp router-id 1.1.1.1

! Unequal-cost load balancing
Router(config-router)# variance 2   ! Include routes up to 2x the FD

! Verification
Router# show ip eigrp neighbors
Router# show ip eigrp topology
Router# show ip eigrp topology all-links
Router# show ip route eigrp
```

### EIGRP Packet Types

| Type | Name | Purpose |
|------|------|---------|
| Hello | Neighbor discovery | Discover/maintain neighbors |
| Update | Route updates | Send routes (reliable) |
| Query | Route query | Ask for routes (when successor lost) |
| Reply | Query response | Respond to queries |
| ACK | Acknowledgment | Confirm reliable packets |

---

## 2. OSPF Advanced

### OSPF LSA Types Deep Dive

```
┌─────────────────────────────────────────────────────────────┐
│                      OSPF LSA Types                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Type 1 - Router LSA:                                      │
│  • Generated by every router                               │
│  • Describes router's interfaces in an area               │
│  • Stays within area                                       │
│                                                             │
│  Type 2 - Network LSA:                                     │
│  • Generated by DR on multi-access networks               │
│  • Lists all routers on the segment                       │
│  • Stays within area                                       │
│                                                             │
│  Type 3 - Summary LSA:                                     │
│  • Generated by ABR                                        │
│  • Advertises inter-area routes                           │
│  • Does NOT contain detailed topology                     │
│                                                             │
│  Type 4 - ASBR Summary LSA:                                │
│  • Generated by ABR                                        │
│  • Locates ASBRs for other areas                          │
│                                                             │
│  Type 5 - External LSA:                                    │
│  • Generated by ASBR                                       │
│  • External routes (redistributed)                         │
│  • Flooded throughout OSPF domain                         │
│                                                             │
│  Type 7 - NSSA External LSA:                               │
│  • Generated by ASBR in NSSA                              │
│  • Converted to Type 5 at ABR                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### OSPF Area Types

```
┌─────────────────────────────────────────────────────────────┐
│                    OSPF Area Types                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Standard Area:                                             │
│  • Receives all LSA types                                  │
│                                                             │
│  Stub Area:                                                 │
│  • No Type 5 LSAs (external routes)                        │
│  • ABR injects default route                               │
│  • Reduces LSDB size                                       │
│                                                             │
│  Totally Stubby Area (Cisco):                              │
│  • No Type 3, 4, 5 LSAs                                    │
│  • Only default route from ABR                             │
│  • Maximum LSDB reduction                                  │
│                                                             │
│  NSSA (Not-So-Stubby Area):                                │
│  • No Type 5, but allows local redistribution             │
│  • Uses Type 7 LSA (converted to Type 5 at ABR)           │
│                                                             │
│  Totally NSSA:                                              │
│  • NSSA + no Type 3 (only default + Type 7)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### OSPF Area Configuration

```cisco
! Stub Area
Router(config)# router ospf 1
Router(config-router)# area 1 stub

! Totally Stubby Area (on ABR only)
Router(config-router)# area 1 stub no-summary

! NSSA
Router(config-router)# area 2 nssa

! Totally NSSA (on ABR)
Router(config-router)# area 2 nssa no-summary

! Summarization at ABR
Router(config-router)# area 1 range 10.1.0.0 255.255.0.0

! Summarization at ASBR (external)
Router(config-router)# summary-address 192.168.0.0 255.255.0.0
```

### OSPF Path Selection

```
OSPF Route Preference (lowest to highest cost):
1. Intra-area (O)
2. Inter-area (O IA)
3. External Type 1 (O E1) - metric includes internal cost
4. External Type 2 (O E2) - metric is external only (default)
5. NSSA Type 1 (O N1)
6. NSSA Type 2 (O N2)
```

---

## 3. BGP

### BGP Overview

```
BGP (Border Gateway Protocol):
- THE routing protocol of the Internet
- Path-vector protocol
- Uses TCP port 179
- External BGP (eBGP) - between ASes
- Internal BGP (iBGP) - within AS

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│        AS 65001                    AS 65002                │
│   ┌─────────────────┐         ┌─────────────────┐          │
│   │  ┌───┐   ┌───┐  │  eBGP   │  ┌───┐   ┌───┐  │          │
│   │  │R1 │───│R2 │──┼─────────┼──│R3 │───│R4 │  │          │
│   │  └───┘   └───┘  │         │  └───┘   └───┘  │          │
│   │     iBGP        │         │      iBGP       │          │
│   └─────────────────┘         └─────────────────┘          │
│                                                             │
│   eBGP: Between autonomous systems (AD = 20)               │
│   iBGP: Within autonomous system (AD = 200)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### BGP Path Attributes

```
BGP Path Selection (in order):
┌─────────────────────────────────────────────────────────────┐
│ #  │ Attribute              │ Prefer                       │
├─────────────────────────────────────────────────────────────┤
│ 1  │ Weight (Cisco only)    │ Highest                      │
│ 2  │ Local Preference       │ Highest                      │
│ 3  │ Locally originated     │ Prefer local routes          │
│ 4  │ AS-Path length         │ Shortest                     │
│ 5  │ Origin type            │ IGP (i) > EGP (e) > ? (?)    │
│ 6  │ MED                    │ Lowest                       │
│ 7  │ eBGP over iBGP         │ Prefer eBGP                  │
│ 8  │ IGP metric to next-hop │ Lowest                       │
│ 9  │ Oldest route           │ Prefer older                 │
│ 10 │ Router ID              │ Lowest                       │
│ 11 │ Neighbor IP            │ Lowest                       │
└─────────────────────────────────────────────────────────────┘

Mnemonic: "We Love Oranges AS Oranges Mean Pure Refreshment"
Weight, Local pref, Originated, AS-path, Origin, MED, Paths (eBGP), Rid
```

### BGP Configuration

```cisco
! Basic BGP Configuration
Router(config)# router bgp 65001
Router(config-router)# bgp router-id 1.1.1.1
Router(config-router)# no bgp default ipv4-unicast

! eBGP Neighbor
Router(config-router)# neighbor 203.0.113.2 remote-as 65002
Router(config-router)# neighbor 203.0.113.2 description ISP-A
Router(config-router)# neighbor 203.0.113.2 update-source Loopback0
Router(config-router)# neighbor 203.0.113.2 ebgp-multihop 2

! iBGP Neighbor
Router(config-router)# neighbor 10.0.0.2 remote-as 65001
Router(config-router)# neighbor 10.0.0.2 update-source Loopback0
Router(config-router)# neighbor 10.0.0.2 next-hop-self

! Address Family
Router(config-router)# address-family ipv4 unicast
Router(config-router-af)# neighbor 203.0.113.2 activate
Router(config-router-af)# neighbor 10.0.0.2 activate
Router(config-router-af)# network 192.168.1.0 mask 255.255.255.0

! Verification
Router# show bgp summary
Router# show bgp ipv4 unicast
Router# show bgp ipv4 unicast neighbors
Router# show bgp ipv4 unicast 192.168.1.0
```

### BGP Path Manipulation

```cisco
! Weight (local router only)
Router(config)# route-map SET-WEIGHT permit 10
Router(config-route-map)# set weight 200
Router(config)# router bgp 65001
Router(config-router)# neighbor 203.0.113.2 route-map SET-WEIGHT in

! Local Preference (iBGP)
Router(config)# route-map SET-LP permit 10
Router(config-route-map)# set local-preference 200
Router(config)# router bgp 65001
Router(config-router)# neighbor 203.0.113.2 route-map SET-LP in

! AS-Path Prepending (make path look longer)
Router(config)# route-map PREPEND permit 10
Router(config-route-map)# set as-path prepend 65001 65001 65001
Router(config)# router bgp 65001
Router(config-router)# neighbor 203.0.113.2 route-map PREPEND out

! MED (outbound to influence inbound)
Router(config)# route-map SET-MED permit 10
Router(config-route-map)# set metric 100
Router(config)# router bgp 65001
Router(config-router)# neighbor 203.0.113.2 route-map SET-MED out
```

---

## 4. Route Redistribution

### Redistribution Overview

```
Redistribution connects different routing domains

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     OSPF Domain              EIGRP Domain                  │
│   ┌───────────────┐       ┌───────────────┐                │
│   │               │       │               │                │
│   │  R1 ─── R2 ───┼───────┼─── R3 ─── R4  │                │
│   │               │  ABR  │               │                │
│   └───────────────┘       └───────────────┘                │
│                       │                                     │
│                       │                                     │
│              Redistribution Point                          │
│              (careful with metrics!)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Redistribution Configuration

```cisco
! Redistribute EIGRP into OSPF
Router(config)# router ospf 1
Router(config-router)# redistribute eigrp 100 subnets metric 100 metric-type 1

! Redistribute OSPF into EIGRP
Router(config)# router eigrp 100
Router(config-router)# redistribute ospf 1 metric 10000 100 255 1 1500

! Redistribute Static into OSPF
Router(config)# router ospf 1
Router(config-router)# redistribute static subnets

! Redistribute Connected into BGP
Router(config)# router bgp 65001
Router(config-router)# address-family ipv4
Router(config-router-af)# redistribute connected

! Default Seed Metrics
! OSPF: metric 20, type E2
! EIGRP: Infinity (must specify)
! BGP: Uses IGP metric
```

### Redistribution Best Practices

```
⚠️ REDISTRIBUTION WARNINGS:

1. Always use route-maps for control
2. Set appropriate metrics
3. Be aware of routing loops
4. Use tags to prevent feedback loops
5. Document thoroughly!

Route Tagging to Prevent Loops:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Router(config)# route-map OSPF-TO-EIGRP permit 10         │
│  Router(config-route-map)# match tag 100                   │
│  Router(config-route-map)# deny    ! Don't redistribute   │
│                                                             │
│  Router(config)# route-map OSPF-TO-EIGRP permit 20         │
│  Router(config-route-map)# set tag 200                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Route Filtering

### Filtering Methods

| Method | Scope | Use |
|--------|-------|-----|
| Distribute-list | Interface/routing process | Filter specific routes |
| Prefix-list | In/Out | Efficient prefix matching |
| Route-map | Flexible | Complex filtering/manipulation |
| Filter-list | BGP | Filter by AS-path |

### Prefix-List Configuration

```cisco
! Permit a specific prefix
ip prefix-list FILTER seq 5 permit 192.168.1.0/24

! Permit range of prefix lengths
ip prefix-list FILTER seq 10 permit 10.0.0.0/8 ge 16 le 24

! Deny default route
ip prefix-list FILTER seq 15 deny 0.0.0.0/0

! Permit everything else
ip prefix-list FILTER seq 100 permit 0.0.0.0/0 le 32

! Apply to OSPF
Router(config)# router ospf 1
Router(config-router)# distribute-list prefix FILTER in

! Apply to BGP
Router(config)# router bgp 65001
Router(config-router)# neighbor 10.0.0.2 prefix-list FILTER in
```

### AS-Path Filtering (BGP)

```cisco
! Filter routes from specific AS
ip as-path access-list 1 deny _65002_
ip as-path access-list 1 permit .*

! Apply to BGP neighbor
Router(config)# router bgp 65001
Router(config-router)# neighbor 10.0.0.2 filter-list 1 in

! Regular expressions:
! ^       Start of AS-path
! $       End of AS-path
! _       Any delimiter
! .       Any character
! *       Zero or more of previous
! +       One or more of previous
! ?       Zero or one of previous
! [0-9]   Character class
```

---

## 6. Multicast

### Multicast Overview

```
Unicast: One-to-one (1 sender, 1 receiver)
Broadcast: One-to-all (1 sender, all receivers)
Multicast: One-to-many (1 sender, interested receivers)

Multicast IP Ranges:
224.0.0.0 - 239.255.255.255 (Class D)

Reserved:
224.0.0.1   All hosts
224.0.0.2   All routers
224.0.0.5   OSPF all routers
224.0.0.6   OSPF DRs
224.0.0.9   RIPv2
224.0.0.10  EIGRP
224.0.0.13  PIMv2
```

### PIM (Protocol Independent Multicast)

```
PIM Modes:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Dense Mode (PIM-DM):                                      │
│  • Flood and prune                                         │
│  • Not scalable, legacy                                    │
│                                                             │
│  Sparse Mode (PIM-SM):                                     │
│  • Pull model (explicit join)                              │
│  • Uses RP (Rendezvous Point)                             │
│  • Scalable, preferred                                     │
│                                                             │
│  Sparse-Dense Mode:                                        │
│  • Operates in either mode                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Basic Multicast Configuration

```cisco
! Enable multicast routing
Router(config)# ip multicast-routing

! Enable PIM on interface
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip pim sparse-mode

! Configure RP (static)
Router(config)# ip pim rp-address 10.0.0.1

! Auto-RP (dynamic RP discovery)
Router(config)# ip pim send-rp-announce Loopback0 scope 16
Router(config)# ip pim send-rp-discovery Loopback0 scope 16

! Verification
Router# show ip mroute
Router# show ip pim neighbor
Router# show ip pim rp mapping
Router# show ip igmp groups
```

---

## 📝 Module 3 Exercises

### Exercise 3.1: EIGRP
Configure EIGRP with:
- Named mode
- Unequal cost load balancing (variance 2)
- Stub sites
- Summarization

### Exercise 3.2: OSPF Areas
Build a multi-area OSPF network with:
- Area 0 (backbone)
- Area 1 (stub)
- Area 2 (NSSA with redistribution)
- Summarization at ABR

### Exercise 3.3: BGP
Configure eBGP/iBGP:
- eBGP with ISP
- iBGP full mesh
- Influence path selection with Local Pref and AS-prepend

### Exercise 3.4: Redistribution
Redistribute between OSPF and EIGRP:
- Use route-maps
- Set appropriate metrics
- Implement loop prevention with tags

---

*Previous: [← Virtualization](../02-virtualization/README.md) | Next: [Network Assurance →](../04-network-assurance/README.md)*

