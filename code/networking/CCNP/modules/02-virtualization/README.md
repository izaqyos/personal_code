# Module 2: Virtualization 🌐

> **20% of ENCOR Exam | Estimated Time: 40-50 hours**

## Module Overview

This module covers network virtualization technologies including VRF, tunneling, and overlay protocols. These are mostly new topics not covered in CCNA.

---

## Table of Contents

1. [VRF & VRF-Lite](#1-vrf--vrf-lite)
2. [GRE Tunnels](#2-gre-tunnels)
3. [IPsec VPN](#3-ipsec-vpn)
4. [DMVPN](#4-dmvpn)
5. [LISP](#5-lisp)
6. [VXLAN](#6-vxlan)

---

## 1. VRF & VRF-Lite

### VRF Concepts

```
VRF (Virtual Routing and Forwarding):
- Multiple routing tables on one router
- Traffic isolation without physical separation
- Each VRF = independent routing instance

Without VRF:                      With VRF:
┌─────────────────────┐          ┌─────────────────────┐
│      Router         │          │      Router         │
│ ┌─────────────────┐ │          │ ┌───────┐ ┌───────┐ │
│ │ Single Routing  │ │          │ │VRF-A  │ │VRF-B  │ │
│ │ Table           │ │          │ │Routes │ │Routes │ │
│ └─────────────────┘ │          │ └───────┘ └───────┘ │
└─────────────────────┘          └─────────────────────┘
All traffic can                   Isolated - A can't 
reach all networks               reach B
```

### VRF-Lite Configuration

```cisco
! Create VRF
Router(config)# vrf definition CUSTOMER-A
Router(config-vrf)# rd 65000:1
Router(config-vrf)# address-family ipv4
Router(config-vrf-af)# exit
Router(config-vrf)# address-family ipv6
Router(config-vrf-af)# exit

! Assign interface to VRF
Router(config)# interface GigabitEthernet0/0
Router(config-if)# vrf forwarding CUSTOMER-A
! Note: This removes IP address, must re-add
Router(config-if)# ip address 192.168.1.1 255.255.255.0

! VRF-aware routing
Router(config)# router ospf 1 vrf CUSTOMER-A
Router(config-router)# network 192.168.1.0 0.0.0.255 area 0

! Verification
Router# show vrf
Router# show ip route vrf CUSTOMER-A
Router# ping vrf CUSTOMER-A 192.168.1.10
```

### VRF Route Leaking

```cisco
! Import routes from another VRF
Router(config)# vrf definition CUSTOMER-A
Router(config-vrf)# address-family ipv4
Router(config-vrf-af)# import ipv4 unicast map IMPORT-FROM-B

! Route-map for selective import
Router(config)# route-map IMPORT-FROM-B permit 10
Router(config-route-map)# match ip address prefix-list SHARED-SERVICES
```

---

## 2. GRE Tunnels

### GRE Overview

```
GRE (Generic Routing Encapsulation):
- Encapsulates any L3 protocol inside IP
- Adds 24-byte header
- Supports multicast/broadcast
- No encryption (use with IPsec for security)

Original Packet:
┌─────────────────────────────────────────────┐
│ IP Header │ TCP/UDP │ Data                  │
└─────────────────────────────────────────────┘

GRE Encapsulated:
┌───────────────────────────────────────────────────────────┐
│ New IP │ GRE Hdr │ Original IP │ TCP/UDP │ Data          │
│ Header │ (4-24B) │   Header    │         │               │
└───────────────────────────────────────────────────────────┘
```

### GRE Configuration

```cisco
! Site A Router
Router-A(config)# interface Tunnel0
Router-A(config-if)# ip address 10.0.0.1 255.255.255.252
Router-A(config-if)# tunnel source GigabitEthernet0/0
Router-A(config-if)# tunnel destination 203.0.113.2
Router-A(config-if)# tunnel mode gre ip
! Optional: Set MTU and MSS
Router-A(config-if)# ip mtu 1400
Router-A(config-if)# ip tcp adjust-mss 1360

! Site B Router
Router-B(config)# interface Tunnel0
Router-B(config-if)# ip address 10.0.0.2 255.255.255.252
Router-B(config-if)# tunnel source GigabitEthernet0/0
Router-B(config-if)# tunnel destination 198.51.100.1
Router-B(config-if)# tunnel mode gre ip

! Verification
Router# show interface tunnel 0
Router# show ip route | include Tunnel
```

---

## 3. IPsec VPN

### IPsec Framework

```
┌─────────────────────────────────────────────────────────────┐
│                     IPsec Components                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  IKE (Internet Key Exchange):                              │
│  ├── Phase 1: Establish secure channel (ISAKMP SA)        │
│  │   - Authentication (PSK or Certificates)               │
│  │   - Diffie-Hellman key exchange                        │
│  │   - Creates IKE SA                                     │
│  │                                                         │
│  └── Phase 2: Negotiate IPsec SA                          │
│      - Quick Mode                                          │
│      - Creates IPsec SA pair (one each direction)         │
│                                                             │
│  IPsec Protocols:                                          │
│  ├── AH (Auth Header): Integrity only, protocol 51        │
│  └── ESP (Encap Sec Payload): Encrypt + integrity, prot 50│
│                                                             │
│  Modes:                                                     │
│  ├── Transport: Original IP header preserved              │
│  └── Tunnel: New IP header added (site-to-site)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### IKEv2 Site-to-Site Configuration

```cisco
! Step 1: IKEv2 Proposal (encryption/integrity/DH)
Router(config)# crypto ikev2 proposal PROP1
Router(config-ikev2-proposal)# encryption aes-cbc-256
Router(config-ikev2-proposal)# integrity sha384
Router(config-ikev2-proposal)# group 19

! Step 2: IKEv2 Policy
Router(config)# crypto ikev2 policy POL1
Router(config-ikev2-policy)# proposal PROP1

! Step 3: IKEv2 Keyring (PSK)
Router(config)# crypto ikev2 keyring KEYS
Router(config-ikev2-keyring)# peer SITE-B
Router(config-ikev2-keyring-peer)# address 203.0.113.2
Router(config-ikev2-keyring-peer)# pre-shared-key MySecretKey123

! Step 4: IKEv2 Profile
Router(config)# crypto ikev2 profile PROF1
Router(config-ikev2-profile)# match identity remote address 203.0.113.2
Router(config-ikev2-profile)# authentication remote pre-share
Router(config-ikev2-profile)# authentication local pre-share
Router(config-ikev2-profile)# keyring local KEYS

! Step 5: IPsec Transform Set
Router(config)# crypto ipsec transform-set TSET esp-aes 256 esp-sha384-hmac
Router(cfg-crypto-trans)# mode tunnel

! Step 6: IPsec Profile (for tunnel interface)
Router(config)# crypto ipsec profile IPSEC-PROF
Router(ipsec-profile)# set transform-set TSET
Router(ipsec-profile)# set ikev2-profile PROF1

! Step 7: Apply to GRE Tunnel (GRE over IPsec)
Router(config)# interface Tunnel0
Router(config-if)# tunnel protection ipsec profile IPSEC-PROF

! Verification
Router# show crypto ikev2 sa
Router# show crypto ipsec sa
Router# show crypto session
```

---

## 4. DMVPN

### DMVPN Overview

```
DMVPN (Dynamic Multipoint VPN):
- Combines GRE + NHRP + IPsec
- Hub-and-spoke with dynamic spoke-to-spoke tunnels
- Single tunnel interface at hub

Phase 1: Hub-and-Spoke only
Phase 2: Spoke-to-spoke via hub (CEF switching)
Phase 3: Spoke-to-spoke direct (NHRP redirect)

      ┌────────────┐
      │    Hub     │
      │  (mGRE)    │
      └─────┬──────┘
           ╱│╲
          ╱ │ ╲
         ╱  │  ╲
        ╱   │   ╲
    ┌──┴─┐ ┌┴──┐ ┌─┴──┐
    │Sp1 │ │Sp2│ │Sp3 │
    │GRE │ │GRE│ │GRE │
    └────┘ └───┘ └────┘
        ╲    │    ╱
         ╲   │   ╱ 
          ╲  │  ╱  Phase 2/3: 
           ╲ │ ╱   Dynamic spoke-to-spoke
            ╲│╱
```

### NHRP (Next Hop Resolution Protocol)

```
NHRP enables dynamic tunnel endpoint discovery

Spoke registers with Hub:
┌────────────────────────────────────────────────────────────┐
│ Spoke1 ──── NHRP Registration ────▶ Hub (NHS)             │
│                                                            │
│ "I'm 10.0.0.2 (tunnel IP) at 198.51.100.10 (NBMA IP)"    │
└────────────────────────────────────────────────────────────┘

Spoke-to-Spoke Resolution:
┌────────────────────────────────────────────────────────────┐
│ Spoke1 ──── NHRP Resolution Request ────▶ Hub             │
│        "Where is 10.0.0.3?"                               │
│                                                            │
│ Spoke1 ◀── NHRP Resolution Reply ──────── Hub             │
│        "10.0.0.3 is at 203.0.113.20"                      │
└────────────────────────────────────────────────────────────┘
```

### DMVPN Hub Configuration

```cisco
! Hub Configuration
Hub(config)# interface Tunnel0
Hub(config-if)# ip address 10.0.0.1 255.255.255.0
Hub(config-if)# ip nhrp network-id 1
Hub(config-if)# ip nhrp map multicast dynamic
Hub(config-if)# ip nhrp redirect          ! Phase 3
Hub(config-if)# tunnel source GigabitEthernet0/0
Hub(config-if)# tunnel mode gre multipoint
Hub(config-if)# tunnel key 100
Hub(config-if)# tunnel protection ipsec profile DMVPN-PROF

! Routing (EIGRP example)
Hub(config)# router eigrp 100
Hub(config-router)# network 10.0.0.0 0.0.0.255
Hub(config-router)# no auto-summary
```

### DMVPN Spoke Configuration

```cisco
! Spoke Configuration
Spoke1(config)# interface Tunnel0
Spoke1(config-if)# ip address 10.0.0.2 255.255.255.0
Spoke1(config-if)# ip nhrp network-id 1
Spoke1(config-if)# ip nhrp nhs 10.0.0.1 nbma 198.51.100.1 multicast
Spoke1(config-if)# ip nhrp shortcut       ! Phase 3
Spoke1(config-if)# tunnel source GigabitEthernet0/0
Spoke1(config-if)# tunnel mode gre multipoint
Spoke1(config-if)# tunnel key 100
Spoke1(config-if)# tunnel protection ipsec profile DMVPN-PROF

! Verification
Router# show dmvpn
Router# show ip nhrp
Router# show crypto session
```

---

## 5. LISP

### LISP Architecture

```
LISP separates device identity (EID) from location (RLOC)

Traditional IP: One address = Identity + Location
LISP:          EID (who) ≠ RLOC (where)

┌─────────────────────────────────────────────────────────────┐
│                     LISP Components                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  EID (Endpoint ID):                                        │
│  • Host address (unchanged when moving)                    │
│                                                             │
│  RLOC (Routing Locator):                                   │
│  • Location in network (tunnel router address)             │
│                                                             │
│  xTR (Tunnel Router):                                      │
│  • ITR: Ingress - encapsulates outbound                   │
│  • ETR: Egress - decapsulates inbound                     │
│  • Can be both (xTR)                                       │
│                                                             │
│  MS (Map Server):                                          │
│  • Stores EID-to-RLOC mappings                            │
│  • ETRs register EIDs with MS                             │
│                                                             │
│  MR (Map Resolver):                                        │
│  • ITRs query MR to resolve EID to RLOC                   │
│  • Often co-located with MS                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### LISP Configuration

```cisco
! Map Server/Map Resolver
MS(config)# router lisp
MS(config-router-lisp)# site SITE-A
MS(config-router-lisp-site)# eid-prefix 10.1.0.0/16
MS(config-router-lisp-site)# authentication-key SITE-A-KEY
MS(config-router-lisp-site)# exit
MS(config-router-lisp)# ipv4 map-server
MS(config-router-lisp)# ipv4 map-resolver

! xTR (Site Router)
xTR(config)# router lisp
xTR(config-router-lisp)# eid-table default instance-id 0
xTR(config-router-lisp-eid-table)# database-mapping 10.1.0.0/16 locator-set RLOC
xTR(config-router-lisp-eid-table)# exit
xTR(config-router-lisp)# locator-set RLOC
xTR(config-router-lisp-locator)# IPv4-interface GigabitEthernet0/0 priority 1 weight 1
xTR(config-router-lisp-locator)# exit
xTR(config-router-lisp)# ipv4 itr map-resolver 192.168.100.1
xTR(config-router-lisp)# ipv4 etr map-server 192.168.100.1 key SITE-A-KEY
xTR(config-router-lisp)# ipv4 itr
xTR(config-router-lisp)# ipv4 etr
```

---

## 6. VXLAN

### VXLAN Overview

```
VXLAN (Virtual eXtensible LAN):
- Layer 2 over Layer 3 overlay
- 24-bit VNI = 16 million segments (vs 4096 VLANs)
- UDP port 4789
- Used in data centers and SD-Access

VXLAN Frame:
┌────────────────────────────────────────────────────────────┐
│Outer │Outer│Outer│ UDP │VXLAN│Inner │Inner│        │      │
│Ether │ IP  │ UDP │ Hdr │ Hdr │Ether │ IP  │ Data   │ FCS  │
│ Hdr  │ Hdr │ Hdr │     │8B   │ Hdr  │ Hdr │        │      │
└────────────────────────────────────────────────────────────┘
 14B    20B   8B    8B          14B+   20B+
 
Total overhead: ~50 bytes
```

### VXLAN Components

```
┌─────────────────────────────────────────────────────────────┐
│                    VXLAN Terminology                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  VTEP (VXLAN Tunnel Endpoint):                             │
│  • Encapsulates/decapsulates VXLAN                         │
│  • Can be hardware (switch) or software                    │
│                                                             │
│  VNI (VXLAN Network Identifier):                           │
│  • 24-bit segment ID                                       │
│  • Maps to VLAN                                            │
│                                                             │
│  NVE (Network Virtualization Edge):                        │
│  • Interface where VXLAN processing occurs                 │
│                                                             │
│  Control Planes:                                           │
│  • Flood-and-Learn (multicast-based)                       │
│  • BGP EVPN (scalable, preferred)                          │
│  • LISP (SD-Access)                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### VXLAN with BGP EVPN (Simplified)

```cisco
! Enable VXLAN
Switch(config)# feature vn-segment-vlan-based
Switch(config)# feature nv overlay

! Map VLAN to VNI
Switch(config)# vlan 100
Switch(config-vlan)# vn-segment 10100

! Configure NVE interface
Switch(config)# interface nve1
Switch(config-if)# source-interface loopback0
Switch(config-if)# member vni 10100
Switch(config-if-nve-vni)# ingress-replication protocol bgp

! BGP EVPN configuration (abbreviated)
Switch(config)# router bgp 65000
Switch(config-router)# neighbor 192.168.1.2 remote-as 65000
Switch(config-router)# address-family l2vpn evpn
Switch(config-router-af)# neighbor 192.168.1.2 activate
```

---

## 📝 Module 2 Exercises

### Exercise 2.1: VRF-Lite
Create two VRFs (CUST-A, CUST-B) and configure:
- Separate routing instances
- OSPF in each VRF
- Route leaking for shared services

### Exercise 2.2: GRE over IPsec
Configure a GRE tunnel with IPsec protection between two sites.

### Exercise 2.3: DMVPN Phase 3
Build a DMVPN network with:
- 1 Hub
- 3 Spokes
- EIGRP for routing
- Verify spoke-to-spoke communication

---

*Previous: [← Architecture](../01-architecture/README.md) | Next: [Infrastructure →](../03-infrastructure/README.md)*

