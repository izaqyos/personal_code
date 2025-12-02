# MPLS (Multiprotocol Label Switching) 🏷️

> **Label-based forwarding for high-performance networks**

## Overview

MPLS operates between Layer 2 and Layer 3 ("Layer 2.5"), using labels instead of IP lookups for fast forwarding.

## MPLS Label

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MPLS Label Format (32 bits)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────────┬─────┬───┬─────────┐                                │
│  │       Label        │ EXP │ S │   TTL   │                                │
│  │     (20 bits)      │(3b) │(1)│ (8 bits)│                                │
│  └────────────────────┴─────┴───┴─────────┘                                │
│                                                                             │
│  Label: Forwarding identifier (0-1,048,575)                                │
│  EXP:   Experimental/Traffic Class (QoS)                                   │
│  S:     Bottom of Stack (1 = last label)                                   │
│  TTL:   Time to Live                                                        │
│                                                                             │
│  Reserved Labels:                                                           │
│  0  = IPv4 Explicit NULL                                                   │
│  1  = Router Alert                                                         │
│  2  = IPv6 Explicit NULL                                                   │
│  3  = Implicit NULL (PHP - Penultimate Hop Popping)                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## MPLS Operations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Label Operations                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PUSH:  Add label to packet                                                │
│         [IP Packet] → [Label][IP Packet]                                   │
│                                                                             │
│  SWAP:  Replace top label                                                  │
│         [Label1][...] → [Label2][...]                                      │
│                                                                             │
│  POP:   Remove top label                                                   │
│         [Label][IP Packet] → [IP Packet]                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## MPLS Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MPLS Network                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CE ─────► PE ═══════► P ═══════► P ═══════► PE ─────► CE                  │
│  (Customer) (Provider Edge)    (Provider Core)    (Provider Edge) (Customer)│
│                                                                             │
│  CE: Customer Edge - normal IP router                                      │
│  PE: Provider Edge - MPLS ingress/egress (LER)                            │
│  P:  Provider - MPLS core (LSR)                                           │
│                                                                             │
│  LER = Label Edge Router (push/pop labels)                                 │
│  LSR = Label Switching Router (swap labels)                                │
│                                                                             │
│  LSP = Label Switched Path (end-to-end path)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Label Distribution Protocols

| Protocol | Description |
|----------|-------------|
| LDP | Label Distribution Protocol - automatic label assignment |
| RSVP-TE | Resource Reservation Protocol - traffic engineering |
| BGP | Carries labels for L3VPN |
| Segment Routing | Uses IGP (no separate protocol) |

### LDP Configuration (Cisco)

```cisco
! Enable MPLS on interface
interface GigabitEthernet0/0
 mpls ip

! Or globally
mpls ldp router-id Loopback0
mpls label protocol ldp

! Verify
show mpls ldp neighbor
show mpls forwarding-table
show mpls ldp bindings
```

## MPLS VPN (L3VPN)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MPLS L3VPN                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Customer A          Provider            Customer A                        │
│  Site 1              Network             Site 2                            │
│  10.1.1.0/24  ──► PE ══════► P ══════► PE ──►  10.1.2.0/24                │
│                     ║                    ║                                  │
│  Customer B         ║                    ║     Customer B                  │
│  Site 1             ║                    ║     Site 2                      │
│  10.1.1.0/24  ──► PE ══════► P ══════► PE ──►  10.1.2.0/24                │
│                                                                             │
│  Same IP space, isolated via VRF + MPLS labels                            │
│                                                                             │
│  Uses two labels:                                                          │
│  - Outer: Transport label (LSP to egress PE)                              │
│  - Inner: VPN label (identifies VRF at egress)                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### L3VPN Configuration

```cisco
! Create VRF
ip vrf CUSTOMER-A
 rd 65000:100
 route-target export 65000:100
 route-target import 65000:100

! Assign interface to VRF
interface GigabitEthernet0/1
 ip vrf forwarding CUSTOMER-A
 ip address 192.168.1.1 255.255.255.0

! PE-CE routing (BGP)
router bgp 65000
 address-family ipv4 vrf CUSTOMER-A
  neighbor 192.168.1.2 remote-as 65001
  neighbor 192.168.1.2 activate

! Verify
show ip vrf
show ip route vrf CUSTOMER-A
show bgp vpnv4 unicast all
```

## MPLS L2VPN (VPWS/VPLS)

| Type | Description |
|------|-------------|
| VPWS | Virtual Private Wire Service - point-to-point |
| VPLS | Virtual Private LAN Service - multipoint |
| EVPN | Ethernet VPN - modern replacement for VPLS |

## Traffic Engineering (RSVP-TE)

```cisco
! Enable MPLS TE
mpls traffic-eng tunnels

interface GigabitEthernet0/0
 mpls traffic-eng tunnels
 ip rsvp bandwidth 1000000

! Create TE tunnel
interface Tunnel0
 ip unnumbered Loopback0
 tunnel mode mpls traffic-eng
 tunnel destination 10.0.0.2
 tunnel mpls traffic-eng bandwidth 100000
 tunnel mpls traffic-eng path-option 1 explicit name PATH1
```

## Segment Routing (Modern MPLS)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Segment Routing                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  No LDP/RSVP needed - labels distributed via IGP (ISIS/OSPF)              │
│                                                                             │
│  Segment Types:                                                             │
│  • Node SID: Identifies a node                                             │
│  • Adjacency SID: Identifies a link                                        │
│  • Prefix SID: Identifies a prefix                                         │
│                                                                             │
│  Benefits:                                                                  │
│  • Simpler (no LDP sessions)                                               │
│  • Source routing (path encoded in header)                                 │
│  • Better TE without state in core                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Next: [TDM (E1/T1) →](./tdm.md)*

