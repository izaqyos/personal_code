# Module 5: Security Fundamentals 🔒

> **15% of CCNA Exam | Estimated Time: 6-8 hours**

## Module Overview

Security has evolved significantly. Key focus areas:
- **Layer 2 security** - DHCP snooping, DAI, port security
- **Wireless security** - WPA3, 802.1X
- **VPN concepts** - New to CCNA

---

## Table of Contents

1. [Security Concepts & Threats](#1-security-concepts--threats)
2. [Access Control Lists](#2-access-control-lists)
3. [Layer 2 Security](#3-layer-2-security)
4. [AAA Concepts](#4-aaa-concepts)
5. [Wireless Security](#5-wireless-security)
6. [VPN Fundamentals](#6-vpn-fundamentals)
7. [Device Hardening](#7-device-hardening)

---

## 1. Security Concepts & Threats

### CIA Triad

```
         Confidentiality
              ╱╲
             ╱  ╲
            ╱    ╲
           ╱      ╲
          ╱   CIA  ╲
         ╱          ╲
        ╱────────────╲
   Integrity      Availability
```

### Common Attack Types

| Attack | Layer | Description | Mitigation |
|--------|-------|-------------|------------|
| MAC Flooding | L2 | Overflow CAM table | Port security |
| VLAN Hopping | L2 | Access other VLANs | Disable DTP |
| DHCP Spoofing | L2 | Rogue DHCP server | DHCP snooping |
| ARP Spoofing | L2 | Fake ARP replies | DAI |
| DDoS | L3-L7 | Overwhelm resources | Firewalls, IPS |
| Man-in-the-Middle | L2-L7 | Intercept traffic | Encryption |
| Password Attack | L7 | Brute force/dictionary | Strong passwords, lockout |

### Security Program Elements

| Element | Description |
|---------|-------------|
| User Awareness | Training employees |
| Physical Security | Lock doors, badge access |
| Network Security | Firewalls, IPS, ACLs |
| Host Security | Antivirus, patching |
| Data Security | Encryption, DLP |

---

## 2. Access Control Lists

### ACL Types

| Type | Number Range | Matches |
|------|--------------|---------|
| Standard | 1-99, 1300-1999 | Source IP only |
| Extended | 100-199, 2000-2699 | Source, Dest, Protocol, Port |
| Named | Name | Standard or Extended |

### Wildcard Masks

```
Wildcard = Inverse of subnet mask
0 = must match
1 = don't care

Examples:
┌────────────────────────────────────────────────────────────┐
│ Match              │ Subnet Mask     │ Wildcard Mask      │
├────────────────────────────────────────────────────────────┤
│ Single host        │ 255.255.255.255 │ 0.0.0.0            │
│ /24 network        │ 255.255.255.0   │ 0.0.0.255          │
│ /16 network        │ 255.255.0.0     │ 0.0.255.255        │
│ /8 network         │ 255.0.0.0       │ 0.255.255.255      │
│ Any                │ 0.0.0.0         │ 255.255.255.255    │
└────────────────────────────────────────────────────────────┘
```

### Standard ACL Configuration

```cisco
! Numbered standard ACL
Router(config)# access-list 10 permit 192.168.1.0 0.0.0.255
Router(config)# access-list 10 deny 192.168.2.0 0.0.0.255
Router(config)# access-list 10 permit any

! Named standard ACL
Router(config)# ip access-list standard ALLOW_NET
Router(config-std-nacl)# permit 192.168.1.0 0.0.0.255
Router(config-std-nacl)# deny any

! Apply to interface (close to destination)
Router(config)# interface gi0/0
Router(config-if)# ip access-group 10 out
```

### Extended ACL Configuration

```cisco
! Syntax
access-list [num] [permit|deny] [protocol] [source] [dest] [options]

! Named extended ACL
Router(config)# ip access-list extended WEB_TRAFFIC
Router(config-ext-nacl)# permit tcp 192.168.1.0 0.0.0.255 any eq 80
Router(config-ext-nacl)# permit tcp 192.168.1.0 0.0.0.255 any eq 443
Router(config-ext-nacl)# deny ip any any log

! Apply to interface (close to source)
Router(config)# interface gi0/1
Router(config-if)# ip access-group WEB_TRAFFIC in

! Common port keywords
eq 80     = HTTP
eq 443    = HTTPS
eq 22     = SSH
eq 23     = Telnet
range 1024 65535 = Port range
```

### ACL Best Practices

```
┌─────────────────────────────────────────────────────────────┐
│                    ACL Rules                                │
├─────────────────────────────────────────────────────────────┤
│ 1. Most specific rules first                               │
│ 2. Standard ACL → close to destination                     │
│ 3. Extended ACL → close to source                          │
│ 4. Implicit deny all at end                                │
│ 5. Only one ACL per interface per direction                │
│ 6. Document your ACLs!                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Layer 2 Security 🔴 FOCUS AREA

### Port Security

```cisco
! Enable port security
Switch(config)# interface fa0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport port-security
Switch(config-if)# switchport port-security maximum 2
Switch(config-if)# switchport port-security mac-address sticky
Switch(config-if)# switchport port-security violation shutdown

! Verify
Switch# show port-security interface fa0/1
Switch# show port-security address
```

| Violation Mode | Action |
|---------------|--------|
| Protect | Drop, no log |
| Restrict | Drop, log |
| Shutdown | Disable port (default) |

### DHCP Snooping

```
DHCP Snooping prevents rogue DHCP servers

          Trusted                    Untrusted
         (to DHCP)                  (to clients)
             │                           │
     ┌───────┴───────┐           ┌───────┴───────┐
     │    gi0/1     │           │    fa0/1-24   │
     │   DHCP OK    │           │  DHCP blocked │
     └───────────────┘           └───────────────┘
```

```cisco
! Enable DHCP snooping
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 10,20

! Configure trusted port (to DHCP server)
Switch(config)# interface gi0/1
Switch(config-if)# ip dhcp snooping trust

! Rate limit on untrusted ports
Switch(config)# interface range fa0/1-24
Switch(config-if-range)# ip dhcp snooping limit rate 15

! Verify
Switch# show ip dhcp snooping
Switch# show ip dhcp snooping binding
```

### Dynamic ARP Inspection (DAI)

```cisco
! Enable DAI (requires DHCP snooping)
Switch(config)# ip arp inspection vlan 10,20

! Trust port (to router/server)
Switch(config)# interface gi0/1
Switch(config-if)# ip arp inspection trust

! Verify
Switch# show ip arp inspection
Switch# show ip arp inspection interfaces
```

### 802.1X Port-Based Authentication

```
┌─────────────────────────────────────────────────────────────┐
│                    802.1X Components                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Supplicant      Authenticator       Authentication       │
│   (Client)        (Switch)            Server (RADIUS)      │
│   ┌────────┐      ┌────────┐          ┌────────┐          │
│   │  PC    │──────│ Switch │──────────│ RADIUS │          │
│   └────────┘      └────────┘          └────────┘          │
│      EAP            EAP                 RADIUS              │
│                                                             │
│   1. Client connects                                        │
│   2. Switch blocks until authenticated                      │
│   3. Client provides credentials                           │
│   4. Switch forwards to RADIUS                             │
│   5. RADIUS validates → success/fail                       │
│   6. Switch opens/denies port                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. AAA Concepts

### AAA Framework

| Component | Purpose |
|-----------|---------|
| **Authentication** | Who are you? (Username/password) |
| **Authorization** | What can you do? (Permissions) |
| **Accounting** | What did you do? (Logging) |

### RADIUS vs TACACS+

| Feature | RADIUS | TACACS+ |
|---------|--------|---------|
| Protocol | UDP 1812/1813 | TCP 49 |
| Encryption | Password only | Full packet |
| AAA | Combined | Separate |
| Vendor | Open standard | Cisco |
| Use | Network access | Device admin |

### AAA Configuration

```cisco
! Enable AAA
Router(config)# aaa new-model

! Configure RADIUS server
Router(config)# radius server RADIUS-SVR
Router(config-radius-server)# address ipv4 10.1.1.100 auth-port 1812 acct-port 1813
Router(config-radius-server)# key MyRadiusKey

! Configure TACACS+ server
Router(config)# tacacs server TACACS-SVR
Router(config-server-tacacs)# address ipv4 10.1.1.101
Router(config-server-tacacs)# key MyTacacsKey

! Configure authentication
Router(config)# aaa authentication login default group radius local
Router(config)# aaa authorization exec default group radius local
Router(config)# aaa accounting exec default start-stop group radius
```

---

## 5. Wireless Security 🔴 NEW TOPIC

### Wireless Security Evolution

```
WEP (1999) → WPA (2003) → WPA2 (2004) → WPA3 (2018)
  │              │              │              │
 Broken      TKIP, MIC      AES-CCMP       SAE, PMF
             (interim)      (current)      (latest)
```

### WPA2 vs WPA3

| Feature | WPA2 | WPA3 |
|---------|------|------|
| Key Exchange | 4-way handshake | SAE (Dragonfly) |
| Encryption | AES-CCMP | AES-GCMP-256 |
| Offline attacks | Vulnerable | Protected |
| Open networks | No encryption | OWE (encrypted) |
| Enterprise | 128-bit | 192-bit mode |

### Authentication Methods

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Personal (PSK)                Enterprise (802.1X)        │
│   ──────────────                ────────────────────        │
│   • Pre-shared key              • RADIUS server            │
│   • Same password for all       • Individual credentials   │
│   • Home/small office           • Certificate-based        │
│                                                             │
│   ┌────────┐                    ┌────────┐    ┌────────┐  │
│   │ Client │──PSK──▶│   AP   │  │ Client │───▶│   AP   │  │
│   └────────┘        └────────┘  └────────┘    └────┬───┘  │
│                                                     │      │
│                                              ┌──────┴────┐ │
│                                              │  RADIUS   │ │
│                                              └───────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. VPN Fundamentals 🔴 NEW TOPIC

### VPN Types

| Type | Description | Use Case |
|------|-------------|----------|
| Site-to-Site | Connects networks | Branch offices |
| Remote Access | User to network | Telecommuters |
| SSL/TLS VPN | Browser-based | Clientless access |
| IPsec VPN | Network layer | Secure tunnels |

### IPsec Components

```
┌─────────────────────────────────────────────────────────────┐
│                     IPsec Framework                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Confidentiality     Integrity        Authentication       │
│  ─────────────────   ──────────       ───────────────       │
│  DES (avoid)         MD5 (avoid)      PSK                   │
│  3DES                SHA-1            RSA                   │
│  AES (recommended)   SHA-256          Certificates          │
│                      SHA-384                                │
│                                                             │
│  Key Exchange: IKE (Internet Key Exchange)                 │
│  ─────────────                                              │
│  Phase 1: Establish secure channel                         │
│  Phase 2: Negotiate IPsec SAs                              │
│                                                             │
│  Protocols:                                                 │
│  ──────────                                                 │
│  AH: Authentication Header (integrity, no encryption)      │
│  ESP: Encapsulating Security Payload (encrypt + auth)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### GRE over IPsec

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Site A                Internet                   Site B   │
│  ┌────────┐    GRE Tunnel (encapsulated)    ┌────────┐    │
│  │ Router │═════════════════════════════════│ Router │    │
│  └────────┘    IPsec (encrypted)            └────────┘    │
│      │                                           │         │
│  192.168.1.0/24                          192.168.2.0/24   │
│                                                             │
│  GRE: Supports multicast, routing protocols               │
│  IPsec: Provides encryption                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Device Hardening

### Password Security

```cisco
! Enable secret (encrypted)
Router(config)# enable secret MySecretPass

! Encrypt plaintext passwords
Router(config)# service password-encryption

! Minimum password length
Router(config)# security passwords min-length 10

! Console password
Router(config)# line console 0
Router(config-line)# password MyConsolePass
Router(config-line)# login
Router(config-line)# exec-timeout 5 0

! VTY password with SSH only
Router(config)# line vty 0 4
Router(config-line)# transport input ssh
Router(config-line)# login local
Router(config-line)# exec-timeout 10 0
```

### Login Security

```cisco
! Failed login lockout
Router(config)# login block-for 120 attempts 3 within 60

! Login delay
Router(config)# login delay 3

! Logging login attempts
Router(config)# login on-failure log
Router(config)# login on-success log
```

### Banner Configuration

```cisco
Router(config)# banner motd #
*****************************************************
*  AUTHORIZED ACCESS ONLY                           *
*  All access is logged and monitored               *
*  Disconnect immediately if not authorized         *
*****************************************************
#
```

### Disable Unused Services

```cisco
! Disable unneeded services
Router(config)# no ip http server
Router(config)# no ip http secure-server
Router(config)# no cdp run
Router(config)# no ip source-route
Router(config)# no service tcp-small-servers
Router(config)# no service udp-small-servers

! Disable unused interfaces
Router(config)# interface gi0/3
Router(config-if)# shutdown
```

---

## 📝 Module 5 Exercises

### Exercise 5.1: Extended ACL
Create an ACL that:
- Allows HTTP/HTTPS from 192.168.1.0/24 to any
- Allows SSH from 10.0.0.0/8 to any
- Denies all other traffic
- Log denied packets

### Exercise 5.2: Layer 2 Security
Configure a switch with:
- Port security (max 2 MACs, sticky)
- DHCP snooping on VLAN 10
- DAI on VLAN 10
- Trust uplink port gi0/1

### Exercise 5.3: Device Hardening
Harden a router with:
- Enable secret
- SSH version 2 only
- 5-minute timeout on console/VTY
- Login lockout after 3 failed attempts
- Warning banner

---

*Previous: [← IP Services](../04-ip-services/README.md) | Next: [Automation →](../06-automation/README.md)*

