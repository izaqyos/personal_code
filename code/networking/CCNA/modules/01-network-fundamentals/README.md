# Module 1: Network Fundamentals 🌐

> **20% of CCNA Exam | Estimated Time: 6-8 hours**

## Module Overview

This module covers the foundational concepts that everything else builds upon. As someone with CCNA experience from 11 years ago, much of this will be familiar, but pay special attention to:
- **IPv6** (now has equal weight to IPv4)
- **Wireless fundamentals** (new to core CCNA)
- **Virtualization concepts** (didn't exist in old CCNA)

---

## Table of Contents

1. [OSI & TCP/IP Models](#1-osi--tcpip-models)
2. [Network Components & Topologies](#2-network-components--topologies)
3. [IPv4 Addressing & Subnetting](#3-ipv4-addressing--subnetting)
4. [IPv6 Addressing](#4-ipv6-addressing)
5. [TCP vs UDP](#5-tcp-vs-udp)
6. [Network Cabling](#6-network-cabling)
7. [Wireless Fundamentals](#7-wireless-fundamentals)
8. [Virtualization Concepts](#8-virtualization-concepts)

---

## 1. OSI & TCP/IP Models

### Quick Refresh: OSI Model

```
Layer 7 - Application    │ HTTP, FTP, SMTP, DNS, DHCP
Layer 6 - Presentation   │ SSL/TLS, JPEG, ASCII, encryption
Layer 5 - Session        │ NetBIOS, RPC, session management
Layer 4 - Transport      │ TCP, UDP, ports, segments
Layer 3 - Network        │ IP, ICMP, routers, packets
Layer 2 - Data Link      │ Ethernet, switches, MAC, frames
Layer 1 - Physical       │ Cables, hubs, bits, signals
```

**Mnemonic**: "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way"

### TCP/IP Model (DoD Model)

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   TCP/IP Model          OSI Equivalent        Protocols     │
│   ─────────────────────────────────────────────────────     │
│   Application           7, 6, 5              HTTP, DNS      │
│   Transport             4                    TCP, UDP       │
│   Internet              3                    IP, ICMP       │
│   Network Access        2, 1                 Ethernet       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Encapsulation

```
Application Data
      ↓ + Header
   Segment (L4) → TCP/UDP header + port numbers
      ↓ + Header
   Packet (L3) → IP header + source/dest IP
      ↓ + Header + Trailer
   Frame (L2) → MAC header + source/dest MAC + FCS
      ↓
   Bits (L1) → Electrical/optical signals
```

### 💡 Key Exam Points
- Know which layer each protocol operates at
- Understand encapsulation/de-encapsulation process
- PDU names: Data → Segment → Packet → Frame → Bits

---

## 2. Network Components & Topologies

### Network Devices

| Device | OSI Layer | Function |
|--------|-----------|----------|
| Hub | L1 | Repeats signals to all ports (obsolete) |
| Switch | L2 | Forwards frames based on MAC address |
| Router | L3 | Forwards packets based on IP address |
| Multilayer Switch | L2-L3 | Switch with routing capability |
| Firewall | L3-L7 | Filters traffic based on rules |
| Wireless AP | L2 | Bridges wireless to wired network |
| WLC | L2-L3 | Manages multiple access points |

### Network Topologies

```
Star Topology (Most Common)
        ┌───┐
        │PC1│
        └─┬─┘
          │
    ┌───┬─┴─┬───┐
    │PC2│ SW│PC3│
    └───┘   └───┘

Mesh Topology (High Availability)
    ┌───┐───────┌───┐
    │R1 │───────│R2 │
    └─┬─┘       └─┬─┘
      │    ╲  ╱   │
      │     ╲╱    │
      │     ╱╲    │
      │    ╱  ╲   │
    ┌─┴─┐       ┌─┴─┐
    │R3 │───────│R4 │
    └───┘       └───┘
```

### Two-Tier vs Three-Tier Architecture

```
Three-Tier (Traditional)          Two-Tier (Spine-Leaf/Modern)
─────────────────────────        ─────────────────────────────
      ┌─────────┐                      ┌────┐   ┌────┐
      │  Core   │                      │Spine│  │Spine│
      └────┬────┘                      └──┬──┘  └──┬──┘
           │                              │╲    ╱│
    ┌──────┴──────┐                       │ ╲  ╱ │
┌───┴───┐    ┌────┴──┐                    │  ╲╱  │
│ Dist  │    │ Dist  │                    │  ╱╲  │
└───┬───┘    └───┬───┘                    │ ╱  ╲ │
    │            │                     ┌──┴──┐┌──┴──┐
┌───┴───┐    ┌───┴───┐                 │Leaf ││Leaf │
│Access │    │Access │                 └─────┘└─────┘
└───────┘    └───────┘
```

---

## 3. IPv4 Addressing & Subnetting

### IPv4 Address Classes (Classful - Legacy)

| Class | Range | Default Mask | Private Range |
|-------|-------|--------------|---------------|
| A | 1-126 | /8 (255.0.0.0) | 10.0.0.0/8 |
| B | 128-191 | /16 (255.255.0.0) | 172.16.0.0/12 |
| C | 192-223 | /24 (255.255.255.0) | 192.168.0.0/16 |

**Note**: 127.x.x.x is reserved for loopback

### CIDR Notation Quick Reference

| CIDR | Subnet Mask | Hosts | Block Size |
|------|-------------|-------|------------|
| /24 | 255.255.255.0 | 254 | 256 |
| /25 | 255.255.255.128 | 126 | 128 |
| /26 | 255.255.255.192 | 62 | 64 |
| /27 | 255.255.255.224 | 30 | 32 |
| /28 | 255.255.255.240 | 14 | 16 |
| /29 | 255.255.255.248 | 6 | 8 |
| /30 | 255.255.255.252 | 2 | 4 |
| /31 | 255.255.255.254 | 2* | 2 |
| /32 | 255.255.255.255 | 1 | 1 |

**Formula**: Hosts = 2^(32-prefix) - 2

### Subnetting Practice

**Example**: Subnet 192.168.10.0/24 into 4 equal subnets

```
Original: 192.168.10.0/24 (256 addresses)
Need: 4 subnets → borrow 2 bits → /26

Result:
┌──────────────────────────────────────────────────────────┐
│ Subnet 1: 192.168.10.0/26   (0-63)    Gateway: .1       │
│ Subnet 2: 192.168.10.64/26  (64-127)  Gateway: .65      │
│ Subnet 3: 192.168.10.128/26 (128-191) Gateway: .129     │
│ Subnet 4: 192.168.10.192/26 (192-255) Gateway: .193     │
└──────────────────────────────────────────────────────────┘
```

### Binary Subnetting Method

```
IP: 192.168.10.130/26

Subnet mask /26 = 255.255.255.192
In binary: 11111111.11111111.11111111.11000000

Host IP:        192.168.10.130 = 11000010.10101000.00001010.10|000010
Subnet mask:                     11111111.11111111.11111111.11|000000
                                                              ↑
                                                    Network|Host boundary

Network:        192.168.10.128 (AND operation)
Broadcast:      192.168.10.191 (OR with inverted mask)
First host:     192.168.10.129
Last host:      192.168.10.190
```

---

## 4. IPv6 Addressing 🔴 FOCUS AREA

### Why IPv6?
- IPv4: ~4.3 billion addresses (exhausted)
- IPv6: 340 undecillion addresses (3.4 × 10^38)

### IPv6 Format

```
Full:        2001:0db8:0000:0000:0000:0000:0000:0001
Compressed:  2001:db8::1

Rules for compression:
1. Remove leading zeros in each group
2. Replace ONE sequence of all-zero groups with ::
```

### IPv6 Address Types

| Type | Prefix | Purpose |
|------|--------|---------|
| Global Unicast | 2000::/3 | Public routable (like public IPv4) |
| Link-Local | fe80::/10 | Auto-configured, single link only |
| Unique Local | fc00::/7 | Private (like RFC1918 in IPv4) |
| Multicast | ff00::/8 | One-to-many |
| Loopback | ::1/128 | Localhost |
| Unspecified | ::/128 | No address assigned |

### EUI-64 Address Generation

```
MAC Address: 00:1A:2B:3C:4D:5E
                 ↓
Split:       00:1A:2B | 3C:4D:5E
                 ↓
Insert FFFE: 00:1A:2B:FF:FE:3C:4D:5E
                 ↓
Flip 7th bit: 02:1A:2B:FF:FE:3C:4D:5E
                 ↓
Interface ID: 021a:2bff:fe3c:4d5e
                 ↓
Full address: fe80::21a:2bff:fe3c:4d5e (link-local)
```

### IPv6 Configuration

```cisco
! Enable IPv6 routing
Router(config)# ipv6 unicast-routing

! Configure interface
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ipv6 address 2001:db8:1::1/64
Router(config-if)# ipv6 address fe80::1 link-local
Router(config-if)# no shutdown

! Verify
Router# show ipv6 interface brief
Router# show ipv6 route
```

### IPv6 vs IPv4 Comparison

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address size | 32 bits | 128 bits |
| Header size | Variable (20-60 bytes) | Fixed (40 bytes) |
| Broadcast | Yes | No (uses multicast) |
| ARP | Yes | No (uses NDP) |
| DHCP | DHCPv4 | DHCPv6 / SLAAC |
| Fragmentation | Router or host | Host only |
| IPsec | Optional | Built-in |

---

## 5. TCP vs UDP

### TCP (Transmission Control Protocol)

```
┌─────────────────────────────────────────────────────────┐
│                    TCP Header (20 bytes)                │
├─────────────────────────────────────────────────────────┤
│ Source Port (16)      │ Destination Port (16)          │
├─────────────────────────────────────────────────────────┤
│ Sequence Number (32)                                    │
├─────────────────────────────────────────────────────────┤
│ Acknowledgment Number (32)                              │
├─────────────────────────────────────────────────────────┤
│ Offset │ Reserved │ Flags │ Window Size (16)           │
├─────────────────────────────────────────────────────────┤
│ Checksum (16)         │ Urgent Pointer (16)            │
└─────────────────────────────────────────────────────────┘

TCP Flags: SYN, ACK, FIN, RST, PSH, URG
```

### TCP Three-Way Handshake

```
Client                              Server
   │                                   │
   │──────── SYN (seq=100) ──────────▶│
   │                                   │
   │◀─── SYN-ACK (seq=300,ack=101) ───│
   │                                   │
   │──────── ACK (ack=301) ──────────▶│
   │                                   │
   │        Connection Established     │
```

### TCP Four-Way Termination

```
Client                              Server
   │                                   │
   │──────── FIN ────────────────────▶│
   │◀─────── ACK ─────────────────────│
   │◀─────── FIN ─────────────────────│
   │──────── ACK ────────────────────▶│
   │                                   │
   │        Connection Closed          │
```

### UDP (User Datagram Protocol)

```
┌─────────────────────────────────────────────────────────┐
│                    UDP Header (8 bytes)                 │
├─────────────────────────────────────────────────────────┤
│ Source Port (16)      │ Destination Port (16)          │
├─────────────────────────────────────────────────────────┤
│ Length (16)           │ Checksum (16)                  │
└─────────────────────────────────────────────────────────┘
```

### Common Port Numbers

| Port | Protocol | Service |
|------|----------|---------|
| 20/21 | TCP | FTP (data/control) |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67/68 | UDP | DHCP (server/client) |
| 69 | UDP | TFTP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 161/162 | UDP | SNMP |
| 443 | TCP | HTTPS |
| 514 | UDP | Syslog |

---

## 6. Network Cabling

### Ethernet Standards

| Standard | Speed | Cable | Max Distance |
|----------|-------|-------|--------------|
| 10BASE-T | 10 Mbps | Cat3 | 100m |
| 100BASE-TX | 100 Mbps | Cat5 | 100m |
| 1000BASE-T | 1 Gbps | Cat5e/6 | 100m |
| 10GBASE-T | 10 Gbps | Cat6a/7 | 100m |
| 25GBASE-T | 25 Gbps | Cat8 | 30m |

### Fiber Optic

| Type | Standard | Distance |
|------|----------|----------|
| Multimode (MMF) | 10GBASE-SR | 400m |
| Single-mode (SMF) | 10GBASE-LR | 10km |
| Single-mode (SMF) | 10GBASE-ER | 40km |

### Cable Types

```
Straight-through: Like devices to unlike
  PC ──────── Switch
  Router ──── Switch

Crossover: Like devices to like
  PC ──────── PC
  Switch ──── Switch
  Router ──── Router

Rollover (Console):
  PC ──────── Router/Switch console port
```

**Note**: Modern devices with Auto-MDIX detect and adjust automatically

---

## 7. Wireless Fundamentals 🔴 NEW TOPIC

### 802.11 Standards

| Standard | Frequency | Max Speed | Year |
|----------|-----------|-----------|------|
| 802.11b | 2.4 GHz | 11 Mbps | 1999 |
| 802.11a | 5 GHz | 54 Mbps | 1999 |
| 802.11g | 2.4 GHz | 54 Mbps | 2003 |
| 802.11n (Wi-Fi 4) | 2.4/5 GHz | 600 Mbps | 2009 |
| 802.11ac (Wi-Fi 5) | 5 GHz | 6.9 Gbps | 2013 |
| 802.11ax (Wi-Fi 6) | 2.4/5/6 GHz | 9.6 Gbps | 2019 |

### Wireless Components

| Component | Function |
|-----------|----------|
| Access Point (AP) | Bridges wireless to wired network |
| Wireless LAN Controller (WLC) | Manages multiple APs centrally |
| Lightweight AP | Controlled by WLC (CAPWAP tunnel) |
| Autonomous AP | Self-contained, standalone config |

### CAPWAP (Control And Provisioning of Wireless APs)

```
┌─────────┐         CAPWAP Tunnel        ┌─────────┐
│   AP    │ ═══════════════════════════  │   WLC   │
│(Lightwt)│    Control + Data Traffic    │         │
└─────────┘                              └─────────┘
     │                                        │
     │ 802.11 (wireless)                      │
     │                                        │
┌─────────┐                              ┌─────────┐
│ Client  │                              │ Network │
└─────────┘                              └─────────┘
```

### Wireless Security

| Method | Description |
|--------|-------------|
| WEP | Deprecated, easily cracked |
| WPA | TKIP encryption, legacy |
| WPA2 | AES encryption, current standard |
| WPA3 | SAE authentication, latest |
| 802.1X | Enterprise auth (RADIUS) |

---

## 8. Virtualization Concepts 🆕 NEW TOPIC

### Virtual Machines vs Containers

```
Virtual Machines                    Containers
┌─────────────────────────┐        ┌─────────────────────────┐
│  ┌─────┐ ┌─────┐ ┌─────┐│        │  ┌─────┐ ┌─────┐ ┌─────┐│
│  │ VM1 │ │ VM2 │ │ VM3 ││        │  │App1 │ │App2 │ │App3 ││
│  │ OS  │ │ OS  │ │ OS  ││        │  └─────┘ └─────┘ └─────┘│
│  └─────┘ └─────┘ └─────┘│        │  Container Runtime      │
│  Hypervisor             │        │  Host OS                │
│  Hardware               │        │  Hardware               │
└─────────────────────────┘        └─────────────────────────┘
```

### Type 1 vs Type 2 Hypervisors

| Type 1 (Bare Metal) | Type 2 (Hosted) |
|---------------------|-----------------|
| VMware ESXi | VMware Workstation |
| Microsoft Hyper-V | VirtualBox |
| KVM | Parallels |
| Runs directly on hardware | Runs on top of OS |

### Cloud Service Models

```
┌─────────────────────────────────────────────────────────────┐
│                    YOU MANAGE ↓                             │
├─────────────────────────────────────────────────────────────┤
│ On-Premises │    IaaS    │    PaaS    │    SaaS            │
├─────────────────────────────────────────────────────────────┤
│ Applications│ Applications│ Applications│ ░░░░░░░░░░░░░░░░│
│ Data        │ Data        │ Data        │ ░░░░░░░░░░░░░░░░│
│ Runtime     │ Runtime     │ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
│ Middleware  │ Middleware  │ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
│ O/S         │ O/S         │ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
│ Virtualiztn │ ░░░░░░░░░░░│ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
│ Servers     │ ░░░░░░░░░░░│ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
│ Storage     │ ░░░░░░░░░░░│ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
│ Networking  │ ░░░░░░░░░░░│ ░░░░░░░░░░░│ ░░░░░░░░░░░░░░░░│
├─────────────────────────────────────────────────────────────┤
│                    PROVIDER MANAGES ↑ (░░░)                 │
└─────────────────────────────────────────────────────────────┘
```

| Model | You Manage | Provider Manages | Example |
|-------|------------|------------------|---------|
| IaaS | Apps, data, OS | Hardware, network | AWS EC2, Azure VMs |
| PaaS | Apps, data | Everything else | Heroku, Google App Engine |
| SaaS | Nothing | Everything | Gmail, Salesforce |

---

## 📝 Module 1 Exercises

### Exercise 1.1: OSI Model Identification
For each scenario, identify the OSI layer:
1. A switch learns a MAC address → Layer ___
2. A router makes a forwarding decision → Layer ___
3. A web browser requests a page → Layer ___
4. Data is encrypted for HTTPS → Layer ___
5. A cable is unplugged → Layer ___

### Exercise 1.2: Subnetting Practice
Subnet the following:
1. 10.0.0.0/8 into 16 subnets
2. 172.16.0.0/16 into subnets with 500 hosts each
3. 192.168.1.0/24 into subnets with 30 hosts each

### Exercise 1.3: IPv6 Compression
Compress these IPv6 addresses:
1. 2001:0db8:0000:0000:0000:0000:0000:0001
2. fe80:0000:0000:0000:0200:00ff:fe00:0001
3. 2001:0db8:aaaa:0001:0000:0000:0000:0100

### Exercise 1.4: Port Numbers
Match the port to the service:
| Port | Service |
|------|---------|
| 443 | ___ |
| 22 | ___ |
| 53 | ___ |
| 67 | ___ |
| 161 | ___ |

---

## 🔗 Additional Resources

- [IPv6 Address Planning](https://www.ripe.net/publications/ipv6-info-centre/)
- [Subnetting Practice Tool](https://subnettingpractice.com/)
- [Wireless Standards Explained](https://www.wi-fi.org/discover-wi-fi)

---

*Next Module: [Network Access →](../02-network-access/README.md)*

