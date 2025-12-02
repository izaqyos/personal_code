# Module 3: IP Connectivity 🛣️

> **25% of CCNA Exam | Estimated Time: 10-12 hours**

## Module Overview

This is the most heavily weighted module on the exam. Key changes since your last CCNA:
- **EIGRP and RIP removed** - Now CCNP only
- **OSPF is the primary focus** - Single-area and multi-area
- **IPv6 routing** - OSPFv3 and static routes

---

## Table of Contents

1. [Static Routing](#1-static-routing)
2. [Dynamic Routing Concepts](#2-dynamic-routing-concepts)
3. [OSPF Single-Area](#3-ospf-single-area)
4. [OSPF Multi-Area](#4-ospf-multi-area)
5. [OSPF Troubleshooting](#5-ospf-troubleshooting)
6. [First Hop Redundancy (HSRP)](#6-first-hop-redundancy-hsrp)
7. [IPv6 Routing](#7-ipv6-routing)

---

## 1. Static Routing

### When to Use Static Routes

| Use Case | Example |
|----------|---------|
| Small networks | Branch offices |
| Stub networks | Single exit point |
| Default routes | Gateway of last resort |
| Backup routes | Floating static routes |

### Static Route Syntax

```cisco
ip route [destination] [mask] [next-hop | exit-interface] [AD]
```

### Types of Static Routes

```cisco
! Standard static route (next-hop)
Router(config)# ip route 192.168.2.0 255.255.255.0 10.1.1.2

! Directly connected static route (exit interface)
Router(config)# ip route 192.168.2.0 255.255.255.0 GigabitEthernet0/0

! Fully specified static route (both)
Router(config)# ip route 192.168.2.0 255.255.255.0 GigabitEthernet0/0 10.1.1.2

! Default route (gateway of last resort)
Router(config)# ip route 0.0.0.0 0.0.0.0 10.1.1.1

! Floating static route (backup with higher AD)
Router(config)# ip route 192.168.2.0 255.255.255.0 10.2.2.2 100
```

### IPv6 Static Routes

```cisco
! Enable IPv6 routing
Router(config)# ipv6 unicast-routing

! IPv6 static route
Router(config)# ipv6 route 2001:db8:2::/64 2001:db8:1::2

! IPv6 default route
Router(config)# ipv6 route ::/0 2001:db8:1::1

! Verify
Router# show ipv6 route static
```

### Administrative Distance

| Route Source | AD |
|--------------|-----|
| Connected | 0 |
| Static | 1 |
| EIGRP summary | 5 |
| eBGP | 20 |
| EIGRP | 90 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| iBGP | 200 |
| Unknown | 255 |

---

## 2. Dynamic Routing Concepts

### Routing Protocol Classification

```
                    Routing Protocols
                          │
          ┌───────────────┴───────────────┐
          │                               │
    Interior (IGP)                  Exterior (EGP)
          │                               │
    ┌─────┴─────┐                        BGP
    │           │
 Distance    Link-State
  Vector
    │           │
   RIP*       OSPF
  EIGRP*      IS-IS

* Not on CCNA anymore
```

### Link-State vs Distance Vector

| Feature | Distance Vector | Link-State |
|---------|-----------------|------------|
| View | Next-hop only | Full topology |
| Updates | Periodic | Event-driven |
| Convergence | Slow | Fast |
| CPU/Memory | Low | Higher |
| Loop Prevention | Split horizon, poison reverse | SPF algorithm |
| Example | RIP, EIGRP | OSPF, IS-IS |

### Routing Protocol Metrics

| Protocol | Metric |
|----------|--------|
| RIP | Hop count |
| EIGRP | Bandwidth + Delay (composite) |
| OSPF | Cost (based on bandwidth) |
| IS-IS | Cost (configurable) |
| BGP | AS path, attributes |

---

## 3. OSPF Single-Area

### OSPF Fundamentals

```
OSPF Process:
1. Discover neighbors (Hello packets)
2. Exchange database information (DBD, LSR, LSU)
3. Calculate shortest path (SPF/Dijkstra)
4. Populate routing table
```

### OSPF Packet Types

| Type | Name | Purpose |
|------|------|---------|
| 1 | Hello | Discover/maintain neighbors |
| 2 | DBD | Database Description |
| 3 | LSR | Link-State Request |
| 4 | LSU | Link-State Update |
| 5 | LSAck | Link-State Acknowledgment |

### OSPF Neighbor States

```
Down → Init → 2-Way → ExStart → Exchange → Loading → Full
  │      │       │        │         │          │        │
  │      │       │        │         │          │        └─ Adjacency formed
  │      │       │        │         │          └─ Exchanging LSAs
  │      │       │        │         └─ Sending DBDs
  │      │       │        └─ Master/slave election
  │      │       └─ Bidirectional communication
  │      └─ Hello received
  └─ No hellos yet
```

### DR/BDR Election

```
On multi-access networks (Ethernet):
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   DR (Designated Router)                                    │
│   • Highest priority (default 1)                           │
│   • If tie, highest Router ID                              │
│   • Receives LSAs on 224.0.0.6                             │
│                                                             │
│   BDR (Backup DR)                                           │
│   • Second highest priority                                 │
│   • Takes over if DR fails                                  │
│                                                             │
│   DROther                                                   │
│   • All other routers                                       │
│   • Only form adjacency with DR/BDR                        │
│   • Send updates to 224.0.0.5                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### OSPF Configuration

```cisco
! Enable OSPF with process ID
Router(config)# router ospf 1

! Configure Router ID (recommended)
Router(config-router)# router-id 1.1.1.1

! Advertise networks
Router(config-router)# network 192.168.1.0 0.0.0.255 area 0
Router(config-router)# network 10.0.0.0 0.0.0.3 area 0

! OR use interface-level configuration (preferred)
Router(config)# interface gi0/0
Router(config-if)# ip ospf 1 area 0

! Set reference bandwidth (for cost calculation)
Router(config-router)# auto-cost reference-bandwidth 10000

! Passive interface (no OSPF on this interface)
Router(config-router)# passive-interface gi0/1

! Verify
Router# show ip ospf neighbor
Router# show ip ospf interface brief
Router# show ip route ospf
Router# show ip ospf database
```

### OSPF Network Types

| Type | DR/BDR | Hello/Dead | Example |
|------|--------|------------|---------|
| Broadcast | Yes | 10/40 | Ethernet |
| Point-to-Point | No | 10/40 | Serial, P2P sub-if |
| NBMA | Yes | 30/120 | Frame Relay |
| Point-to-Multipoint | No | 30/120 | FR, DMVPN |

```cisco
! Change network type
Router(config-if)# ip ospf network point-to-point
```

### OSPF Cost Calculation

```
Cost = Reference Bandwidth / Interface Bandwidth

Default reference: 100 Mbps

Examples:
┌───────────────────────────────────────────────────┐
│ Interface    │ Bandwidth  │ Cost (100M ref)      │
├───────────────────────────────────────────────────┤
│ Serial       │ 1.544 Mbps │ 100/1.544 = 64       │
│ FastEthernet │ 100 Mbps   │ 100/100 = 1          │
│ GigabitEth   │ 1000 Mbps  │ 100/1000 = 1 (!!)    │
│ 10GigE       │ 10000 Mbps │ 100/10000 = 1 (!!)   │
└───────────────────────────────────────────────────┘

Problem: All links >= 100 Mbps have same cost!
Solution: Increase reference bandwidth

Router(config-router)# auto-cost reference-bandwidth 10000

With 10000 Mbps reference:
┌───────────────────────────────────────────────────┐
│ Interface    │ Bandwidth  │ Cost (10G ref)       │
├───────────────────────────────────────────────────┤
│ FastEthernet │ 100 Mbps   │ 10000/100 = 100      │
│ GigabitEth   │ 1000 Mbps  │ 10000/1000 = 10      │
│ 10GigE       │ 10000 Mbps │ 10000/10000 = 1      │
└───────────────────────────────────────────────────┘
```

---

## 4. OSPF Multi-Area

### Why Multi-Area OSPF?

```
Single Area Problems:
• Large LSDB = high memory
• SPF calculation intensive
• Any change triggers full SPF

Multi-Area Benefits:
• Smaller LSDBs per area
• SPF runs within area only
• Summarization at area boundaries
```

### OSPF Area Types

```
                    ┌─────────────────┐
                    │   Area 0        │
                    │  (Backbone)     │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────┴─────┐     ┌──────┴─────┐     ┌──────┴─────┐
    │  Area 1   │     │   Area 2   │     │   Area 3   │
    │ (Normal)  │     │  (Stub)    │     │   (NSSA)   │
    └───────────┘     └────────────┘     └────────────┘
```

### OSPF Router Types

| Type | Description |
|------|-------------|
| Internal Router | All interfaces in same area |
| Backbone Router | At least one interface in Area 0 |
| ABR (Area Border Router) | Interfaces in multiple areas |
| ASBR (AS Boundary Router) | Redistributes external routes |

### LSA Types

| Type | Name | Description |
|------|------|-------------|
| 1 | Router LSA | Every router, stays in area |
| 2 | Network LSA | DR generates for multi-access |
| 3 | Summary LSA | ABR summarizes inter-area |
| 4 | ASBR Summary | Locates ASBRs |
| 5 | External LSA | External routes (ASBR) |
| 7 | NSSA External | External in NSSA areas |

### Multi-Area Configuration

```cisco
! ABR Configuration (connects Area 0 and Area 1)
Router(config)# router ospf 1
Router(config-router)# router-id 2.2.2.2
Router(config-router)# network 10.0.0.0 0.0.0.255 area 0
Router(config-router)# network 192.168.1.0 0.0.0.255 area 1

! Verify
Router# show ip ospf
Router# show ip ospf border-routers
Router# show ip ospf database
```

### Route Summarization

```cisco
! Summarize at ABR (inter-area)
Router(config-router)# area 1 range 192.168.0.0 255.255.252.0

! Summarize at ASBR (external)
Router(config-router)# summary-address 10.0.0.0 255.255.0.0

! Verify
Router# show ip route ospf
```

---

## 5. OSPF Troubleshooting

### Common OSPF Issues

```
┌─────────────────────────────────────────────────────────────┐
│              OSPF Troubleshooting Checklist                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Neighbor Not Forming?                                      │
│  ☐ Layer 1/2 connectivity                                  │
│  ☐ Interface in correct area                               │
│  ☐ Hello/Dead timers match                                 │
│  ☐ Same subnet                                             │
│  ☐ Same area ID                                            │
│  ☐ Same authentication                                     │
│  ☐ MTU match (for full adjacency)                          │
│  ☐ Network type compatible                                 │
│                                                             │
│  Stuck in 2-Way?                                            │
│  • Normal on multi-access with DR/BDR                      │
│  • DROthers stay in 2-Way with each other                  │
│                                                             │
│  Stuck in ExStart/Exchange?                                 │
│  • Usually MTU mismatch                                    │
│  • Check: ip ospf mtu-ignore                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Essential Show Commands

```cisco
! Neighbor status
Router# show ip ospf neighbor
Router# show ip ospf neighbor detail

! Interface information
Router# show ip ospf interface
Router# show ip ospf interface brief

! Database
Router# show ip ospf database
Router# show ip ospf database router
Router# show ip ospf database summary

! Routes
Router# show ip route ospf
Router# show ip route ospf | section 192.168

! Process information
Router# show ip ospf
Router# show ip ospf border-routers
```

### Debug Commands (Use Carefully!)

```cisco
Router# debug ip ospf adj
Router# debug ip ospf hello
Router# debug ip ospf events

! Turn off debugging
Router# undebug all
```

---

## 6. First Hop Redundancy (HSRP)

### Why FHRP?

```
Problem: Single default gateway = single point of failure

         ┌────────────┐
         │   Client   │ Default GW: 192.168.1.1
         └─────┬──────┘
               │
         ┌─────┴──────┐
         │  Switch    │
         └─────┬──────┘
               │
         ┌─────┴──────┐
         │  Router A  │ 192.168.1.1  ← Single point of failure!
         └────────────┘
```

### HSRP Solution

```
         ┌────────────┐
         │   Client   │ Default GW: 192.168.1.254 (Virtual IP)
         └─────┬──────┘
               │
         ┌─────┴──────┐
         │  Switch    │
         └──┬─────┬───┘
            │     │
     ┌──────┴─┐ ┌─┴──────┐
     │Router A│ │Router B│
     │  .1    │ │  .2    │
     │ ACTIVE │ │STANDBY │
     └────────┘ └────────┘
         Both share Virtual IP .254
```

### FHRP Comparison

| Protocol | Standard | Load Balancing | Preemption |
|----------|----------|----------------|------------|
| HSRP | Cisco | Multiple groups | Optional |
| VRRP | RFC 5798 | Multiple groups | Default |
| GLBP | Cisco | Built-in | Optional |

### HSRP Configuration

```cisco
! Router A (Active)
Router(config)# interface gi0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# standby 1 ip 192.168.1.254
Router(config-if)# standby 1 priority 110
Router(config-if)# standby 1 preempt

! Router B (Standby)
Router(config)# interface gi0/0
Router(config-if)# ip address 192.168.1.2 255.255.255.0
Router(config-if)# standby 1 ip 192.168.1.254
Router(config-if)# standby 1 priority 100

! Verify
Router# show standby
Router# show standby brief
```

### HSRP States

```
Initial → Learn → Listen → Speak → Standby → Active
   │        │        │        │        │         │
   │        │        │        │        │         └─ Forwarding traffic
   │        │        │        │        └─ Backup (ready to take over)
   │        │        │        └─ Participating in election
   │        │        └─ Not active/standby, monitoring
   │        └─ Learning virtual IP
   └─ Starting up
```

### HSRP Tracking

```cisco
! Track interface status
Router(config)# track 1 interface gi0/1 line-protocol

! Apply to HSRP
Router(config-if)# standby 1 track 1 decrement 20
```

---

## 7. IPv6 Routing 🔴 FOCUS AREA

### IPv6 Routing Protocols

| Protocol | IPv6 Version |
|----------|--------------|
| Static | Supported |
| RIPng | RIP for IPv6 |
| OSPFv3 | OSPF for IPv6 |
| EIGRP for IPv6 | Cisco |
| MP-BGP | Multi-protocol BGP |

### OSPFv3 Configuration

```cisco
! Enable IPv6 routing
Router(config)# ipv6 unicast-routing

! Enable OSPFv3
Router(config)# ipv6 router ospf 1
Router(config-rtr)# router-id 1.1.1.1

! Configure interface
Router(config)# interface gi0/0
Router(config-if)# ipv6 address 2001:db8:1::1/64
Router(config-if)# ipv6 ospf 1 area 0

! Verify
Router# show ipv6 ospf neighbor
Router# show ipv6 ospf interface brief
Router# show ipv6 route ospf
```

### OSPFv3 vs OSPFv2

| Feature | OSPFv2 | OSPFv3 |
|---------|--------|--------|
| Address family | IPv4 only | IPv6 (and IPv4 with AF) |
| Source | IPv4 | Link-local IPv6 |
| Multicast | 224.0.0.5/6 | FF02::5/6 |
| Authentication | In protocol | IPsec |
| Network statement | Under router ospf | Per interface |
| LSA flooding | Per subnet | Per link |

### IPv6 Static Routing Summary

```cisco
! IPv6 static route examples
ipv6 route 2001:db8:2::/64 2001:db8:1::2           ! Next-hop
ipv6 route 2001:db8:2::/64 gi0/0                   ! Exit interface
ipv6 route 2001:db8:2::/64 gi0/0 2001:db8:1::2     ! Fully specified
ipv6 route ::/0 2001:db8:1::1                      ! Default route
```

---

## 📝 Module 3 Exercises

### Exercise 3.1: Static Routing
Configure static routes for this topology:
```
R1 (10.1.1.1) ------- R2 (10.1.1.2/10.2.2.1) ------- R3 (10.2.2.2)
     |                                                      |
192.168.1.0/24                                     192.168.2.0/24
```

### Exercise 3.2: OSPF Single-Area
Configure single-area OSPF:
1. Enable OSPF process 1
2. Set router-id
3. Advertise all connected networks in area 0
4. Make LAN interface passive
5. Verify neighbor adjacency

### Exercise 3.3: OSPF Multi-Area
Design a multi-area OSPF network:
- Area 0: Backbone (2 routers)
- Area 1: Branch office (3 routers)
- Configure ABR
- Summarize Area 1 routes

### Exercise 3.4: HSRP
Configure HSRP between two routers:
- Virtual IP: 192.168.1.254
- R1: Active (priority 110)
- R2: Standby (priority 100)
- Enable preemption

### Exercise 3.5: IPv6 OSPF
Configure OSPFv3:
1. Enable IPv6 routing
2. Configure OSPFv3 process
3. Assign IPv6 addresses
4. Enable OSPFv3 on interfaces
5. Verify IPv6 routes

---

## 🔗 Additional Resources

- [OSPF Design Guide](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/7039-1.html)
- [IPv6 Addressing Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipv6_basic/configuration/xe-3s/ip6b-xe-3s-book/ip6-add-basic-conn-xe.html)
- [HSRP Configuration Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhp-xe-16-book/fhp-hsrp.html)

---

*Previous: [← Network Access](../02-network-access/README.md) | Next: [IP Services →](../04-ip-services/README.md)*

