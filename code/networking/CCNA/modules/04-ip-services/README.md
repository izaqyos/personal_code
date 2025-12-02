# Module 4: IP Services 🔧

> **10% of CCNA Exam | Estimated Time: 6-8 hours**

## Module Overview

This module covers essential network services. Most concepts will be familiar, but pay attention to:
- **DHCPv6** - Stateful and stateless modes
- **QoS concepts** - New to CCNA curriculum

---

## Table of Contents

1. [NAT/PAT](#1-natpat)
2. [DHCP](#2-dhcp)
3. [DNS](#3-dns)
4. [NTP](#4-ntp)
5. [SNMP & Syslog](#5-snmp--syslog)
6. [QoS Concepts](#6-qos-concepts)
7. [SSH Configuration](#7-ssh-configuration)

---

## 1. NAT/PAT

### NAT Types

| Type | Description | Use Case |
|------|-------------|----------|
| Static NAT | 1:1 mapping | Servers needing external access |
| Dynamic NAT | Pool of addresses | Limited public IPs |
| PAT/NAT Overload | Many:1 with ports | Most common (home routers) |

### NAT Terminology

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Inside Local    │ Inside Global  │ Outside Global         │
│  (Private IP)    │ (Public IP)    │ (Internet IP)          │
│  192.168.1.10    │ 203.0.113.5    │ 8.8.8.8               │
│                  │                │                        │
│  ┌────────┐      │   ┌────────┐   │   ┌────────┐          │
│  │  PC    │──────┼───│ Router │───┼───│ Server │          │
│  └────────┘      │   └────────┘   │   └────────┘          │
│   Inside         │    NAT         │    Outside             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Static NAT Configuration

```cisco
! Define inside and outside interfaces
Router(config)# interface gi0/0
Router(config-if)# ip nat inside
Router(config)# interface gi0/1
Router(config-if)# ip nat outside

! Create static mapping
Router(config)# ip nat inside source static 192.168.1.10 203.0.113.10

! Verify
Router# show ip nat translations
Router# show ip nat statistics
```

### PAT (NAT Overload) Configuration

```cisco
! Define ACL for internal addresses
Router(config)# access-list 1 permit 192.168.1.0 0.0.0.255

! Configure PAT using outside interface
Router(config)# ip nat inside source list 1 interface gi0/1 overload

! OR using a pool
Router(config)# ip nat pool MYPOOL 203.0.113.1 203.0.113.5 netmask 255.255.255.0
Router(config)# ip nat inside source list 1 pool MYPOOL overload
```

---

## 2. DHCP

### DHCP Process (DORA)

```
Client                              Server
   │                                   │
   │──────── DISCOVER (broadcast) ────▶│
   │                                   │
   │◀──────── OFFER (unicast) ─────────│
   │                                   │
   │──────── REQUEST (broadcast) ─────▶│
   │                                   │
   │◀───────── ACK (unicast) ──────────│
   │                                   │
```

### DHCP Server Configuration

```cisco
! Create DHCP pool
Router(config)# ip dhcp pool LAN_POOL
Router(dhcp-config)# network 192.168.1.0 255.255.255.0
Router(dhcp-config)# default-router 192.168.1.1
Router(dhcp-config)# dns-server 8.8.8.8 8.8.4.4
Router(dhcp-config)# domain-name example.com
Router(dhcp-config)# lease 7

! Exclude addresses (servers, gateway)
Router(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.10

! Verify
Router# show ip dhcp binding
Router# show ip dhcp pool
Router# show ip dhcp server statistics
```

### DHCP Relay Agent

```cisco
! On the interface receiving DHCP broadcasts
Router(config)# interface gi0/0
Router(config-if)# ip helper-address 10.1.1.100
```

### DHCPv6 🔴 NEW

```
DHCPv6 Modes:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  SLAAC (Stateless)           Stateful DHCPv6               │
│  ─────────────────           ─────────────────              │
│  • Router provides           • DHCPv6 server provides      │
│    prefix via RA               full address                │
│  • Host generates            • Tracks assignments          │
│    interface ID              • Like DHCPv4                 │
│  • No address tracking                                      │
│                                                             │
│  Stateless DHCPv6                                           │
│  ─────────────────                                          │
│  • SLAAC for address                                        │
│  • DHCPv6 for DNS, domain                                   │
│  • "Other config" flag                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```cisco
! Stateless DHCPv6 server
Router(config)# ipv6 dhcp pool IPV6_POOL
Router(config-dhcpv6)# dns-server 2001:4860:4860::8888
Router(config-dhcpv6)# domain-name example.com

! Apply to interface
Router(config)# interface gi0/0
Router(config-if)# ipv6 dhcp server IPV6_POOL
Router(config-if)# ipv6 nd other-config-flag
```

---

## 3. DNS

### DNS Fundamentals

```
DNS Resolution Process:
┌────────────┐         ┌────────────┐         ┌────────────┐
│   Client   │────────▶│  Resolver  │────────▶│ Root (.)   │
└────────────┘         └────────────┘         └────────────┘
                              │                      │
                              │                      ▼
                              │               ┌────────────┐
                              │               │ TLD (.com) │
                              │               └────────────┘
                              │                      │
                              ▼                      ▼
                       ┌────────────┐         ┌────────────┐
                       │   Cache    │◀────────│Authoritative│
                       └────────────┘         └────────────┘
```

### DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | www.example.com → 192.0.2.1 |
| AAAA | IPv6 address | www.example.com → 2001:db8::1 |
| CNAME | Alias | mail.example.com → server1.example.com |
| MX | Mail server | example.com → mail.example.com |
| NS | Name server | example.com → ns1.example.com |
| PTR | Reverse lookup | 192.0.2.1 → www.example.com |

### DNS Configuration on Router

```cisco
! Enable DNS lookup
Router(config)# ip domain-lookup

! Set DNS server
Router(config)# ip name-server 8.8.8.8 8.8.4.4

! Set domain name
Router(config)# ip domain-name example.com

! Static host entry
Router(config)# ip host server1 192.168.1.100
```

---

## 4. NTP

### NTP Hierarchy (Stratum)

```
Stratum 0: Atomic clocks, GPS (reference clocks)
     │
Stratum 1: Directly connected to Stratum 0
     │
Stratum 2: Syncs from Stratum 1
     │
Stratum 3: Syncs from Stratum 2
     ...
Stratum 15: Maximum (16 = unsynchronized)
```

### NTP Configuration

```cisco
! Configure NTP client
Router(config)# ntp server 216.239.35.0

! Configure as NTP server (for other devices)
Router(config)# ntp master 4

! Set timezone
Router(config)# clock timezone EST -5
Router(config)# clock summer-time EDT recurring

! NTP authentication
Router(config)# ntp authenticate
Router(config)# ntp authentication-key 1 md5 MyKey
Router(config)# ntp trusted-key 1
Router(config)# ntp server 10.1.1.1 key 1

! Verify
Router# show ntp status
Router# show ntp associations
Router# show clock detail
```

---

## 5. SNMP & Syslog

### SNMP Versions

| Version | Security | Features |
|---------|----------|----------|
| v1 | Community strings (plain text) | Basic, deprecated |
| v2c | Community strings (plain text) | GetBulk, Inform |
| v3 | Authentication + Encryption | **Recommended** |

### SNMP Configuration

```cisco
! SNMPv2c (basic)
Router(config)# snmp-server community public RO
Router(config)# snmp-server community private RW
Router(config)# snmp-server location "Data Center"
Router(config)# snmp-server contact admin@example.com

! SNMPv3 (secure)
Router(config)# snmp-server group ADMIN v3 priv
Router(config)# snmp-server user admin ADMIN v3 auth sha AuthPass priv aes 128 PrivPass

! Enable traps
Router(config)# snmp-server enable traps
Router(config)# snmp-server host 10.1.1.100 version 2c public
```

### Syslog

```
Severity Levels:
┌────────────────────────────────────────────────────────────┐
│ Level │ Keyword       │ Description                       │
├────────────────────────────────────────────────────────────┤
│   0   │ emergencies   │ System unusable                   │
│   1   │ alerts        │ Immediate action needed           │
│   2   │ critical      │ Critical conditions               │
│   3   │ errors        │ Error conditions                  │
│   4   │ warnings      │ Warning conditions                │
│   5   │ notifications │ Normal but significant            │
│   6   │ informational │ Informational messages            │
│   7   │ debugging     │ Debug messages                    │
└────────────────────────────────────────────────────────────┘
```

```cisco
! Configure syslog server
Router(config)# logging host 10.1.1.100
Router(config)# logging trap informational
Router(config)# logging source-interface gi0/0

! Enable timestamps
Router(config)# service timestamps log datetime msec

! Verify
Router# show logging
```

---

## 6. QoS Concepts 🔴 NEW TOPIC

### QoS Need

```
Without QoS:                    With QoS:
All traffic equal               Traffic prioritized
┌─────────────────┐            ┌─────────────────┐
│ ▓▓▓░▓░▓░▓░░▓▓░ │            │ ▓▓▓▓▓▓░░░░░░░░ │ Voice
│ Video, voice,   │            │ ░░░░░░▓▓▓▓░░░░ │ Video
│ data mixed      │            │ ░░░░░░░░░░░▓▓▓ │ Data
└─────────────────┘            └─────────────────┘
```

### QoS Models

| Model | Description |
|-------|-------------|
| Best Effort | No QoS (default) |
| IntServ | RSVP reservation per flow |
| DiffServ | Per-hop behavior, scalable |

### QoS Mechanisms

```
┌─────────────────────────────────────────────────────────────┐
│                      QoS Pipeline                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Classification    Identify traffic (ACL, NBAR, DSCP)   │
│         │                                                   │
│         ▼                                                   │
│  2. Marking           Tag packets (DSCP, CoS)              │
│         │                                                   │
│         ▼                                                   │
│  3. Policing/Shaping  Rate limiting                        │
│         │                                                   │
│         ▼                                                   │
│  4. Congestion Mgmt   Queuing (priority, weighted)         │
│         │                                                   │
│         ▼                                                   │
│  5. Congestion Avoid  Drop policy (WRED)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### DSCP Values

| DSCP | PHB | Typical Use |
|------|-----|-------------|
| EF (46) | Expedited Forwarding | Voice |
| AF41 (34) | Assured Forwarding | Video |
| AF31 (26) | Assured Forwarding | Critical data |
| AF21 (18) | Assured Forwarding | Business apps |
| DF (0) | Default | Best effort |

---

## 7. SSH Configuration

### SSH vs Telnet

| Feature | Telnet | SSH |
|---------|--------|-----|
| Encryption | None | Yes |
| Port | 23 | 22 |
| Security | Insecure | Secure |
| Use | Never in production | Always |

### SSH Configuration

```cisco
! Set hostname and domain (required for key generation)
Router(config)# hostname R1
R1(config)# ip domain-name example.com

! Generate RSA keys
R1(config)# crypto key generate rsa modulus 2048

! Create local user
R1(config)# username admin privilege 15 secret MyPassword

! Configure VTY lines
R1(config)# line vty 0 4
R1(config-line)# transport input ssh
R1(config-line)# login local

! Set SSH version 2
R1(config)# ip ssh version 2

! Verify
R1# show ip ssh
R1# show ssh
```

---

## 📝 Module 4 Exercises

### Exercise 4.1: NAT Configuration
Configure PAT for internal network 10.0.0.0/24 using the outside interface.

### Exercise 4.2: DHCP Server
Create a DHCP pool with:
- Network: 192.168.1.0/24
- Gateway: 192.168.1.1
- DNS: 8.8.8.8
- Domain: lab.local
- Exclude: .1-.10

### Exercise 4.3: NTP & Syslog
- Configure NTP to sync from pool.ntp.org
- Send syslog to 10.1.1.100
- Set logging level to informational

---

*Previous: [← IP Connectivity](../03-ip-connectivity/README.md) | Next: [Security →](../05-security/README.md)*

