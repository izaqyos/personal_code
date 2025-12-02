# Module 5: Security 🔐

> **20% of ENCOR Exam | Estimated Time: 40-50 hours**

## Module Overview

Advanced security covering control plane protection, identity services, and encryption technologies beyond CCNA level.

---

## Table of Contents

1. [Infrastructure Security](#1-infrastructure-security)
2. [Control Plane Policing (CoPP)](#2-control-plane-policing-copp)
3. [802.1X & Identity Services](#3-8021x--identity-services)
4. [MACsec](#4-macsec)
5. [TrustSec & SGT](#5-trustsec--sgt)

---

## 1. Infrastructure Security

### Device Hardening Checklist

```
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Security                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Management Plane:                                          │
│  ☐ SSH v2 only (disable Telnet)                           │
│  ☐ Strong passwords (Type 8 or 9)                         │
│  ☐ AAA (TACACS+ for admin)                                │
│  ☐ Role-based access control                              │
│  ☐ Timeout on VTY/Console                                 │
│  ☐ Logging and timestamps                                 │
│  ☐ NTP authentication                                     │
│  ☐ Encrypted configuration backups                        │
│                                                             │
│  Control Plane:                                             │
│  ☐ Control Plane Policing (CoPP)                          │
│  ☐ Routing protocol authentication                        │
│  ☐ BFD for fast failure detection                         │
│  ☐ uRPF (Unicast Reverse Path Forwarding)                │
│                                                             │
│  Data Plane:                                                │
│  ☐ ACLs at network boundaries                             │
│  ☐ DHCP snooping                                          │
│  ☐ Dynamic ARP Inspection                                 │
│  ☐ IP Source Guard                                        │
│  ☐ Storm control                                          │
│  ☐ Private VLANs                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### uRPF (Unicast Reverse Path Forwarding)

```
uRPF prevents IP spoofing by verifying source address

Strict Mode:
• Source IP must be reachable via receiving interface
• Best for single-homed networks

Loose Mode:
• Source IP must exist in routing table (any interface)
• Works with asymmetric routing
```

```cisco
! Strict mode (single path)
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip verify unicast source reachable-via rx

! Loose mode (multi-path/asymmetric)
Router(config-if)# ip verify unicast source reachable-via any

! Allow specific sources (ACL)
Router(config)# ip verify unicast source reachable-via rx allow-default 100
```

### Routing Protocol Authentication

```cisco
! OSPF MD5 Authentication
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip ospf authentication message-digest
Router(config-if)# ip ospf message-digest-key 1 md5 SecretKey

! OSPF SHA Authentication (IOS-XE)
Router(config)# key chain OSPF-KEYS
Router(config-keychain)# key 1
Router(config-keychain-key)# key-string SecretKey
Router(config-keychain-key)# cryptographic-algorithm hmac-sha-256
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip ospf authentication key-chain OSPF-KEYS

! EIGRP Authentication
Router(config)# key chain EIGRP-KEYS
Router(config-keychain)# key 1
Router(config-keychain-key)# key-string SecretKey
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip authentication mode eigrp 100 md5
Router(config-if)# ip authentication key-chain eigrp 100 EIGRP-KEYS

! BGP Authentication
Router(config)# router bgp 65001
Router(config-router)# neighbor 10.1.1.2 password SecretKey
```

---

## 2. Control Plane Policing (CoPP)

### CoPP Overview

```
CoPP protects the router's CPU from attack traffic

Without CoPP:                    With CoPP:
┌─────────────────────────┐     ┌─────────────────────────┐
│         CPU             │     │         CPU             │
│   (overwhelmed)         │     │    (protected)          │
│   ████████████████     │     │    ▓▓▓░░░░░░░░░         │
└─────────────────────────┘     └─────────────────────────┘
        ↑                               ↑
   All traffic                    Rate-limited
   to CPU                         by CoPP
```

### CoPP Configuration

```cisco
! Step 1: Classify traffic to control plane
class-map match-all ICMP-CLASS
 match access-group name ICMP-ACL
class-map match-all BGP-CLASS
 match access-group name BGP-ACL
class-map match-all OSPF-CLASS
 match access-group name OSPF-ACL
class-map match-all SSH-CLASS
 match access-group name SSH-ACL

! ACLs for classification
ip access-list extended ICMP-ACL
 permit icmp any any
ip access-list extended BGP-ACL
 permit tcp any eq bgp any
 permit tcp any any eq bgp
ip access-list extended OSPF-ACL
 permit ospf any any
ip access-list extended SSH-ACL
 permit tcp any any eq 22

! Step 2: Define policy
policy-map COPP-POLICY
 class ICMP-CLASS
  police rate 64000 bps burst 8000 bytes
   conform-action transmit
   exceed-action drop
 class BGP-CLASS
  police rate 256000 bps
   conform-action transmit
   exceed-action drop
 class OSPF-CLASS
  police rate 128000 bps
   conform-action transmit
   exceed-action drop
 class SSH-CLASS
  police rate 64000 bps
   conform-action transmit
   exceed-action drop
 class class-default
  police rate 32000 bps
   conform-action transmit
   exceed-action drop

! Step 3: Apply to control plane
control-plane
 service-policy input COPP-POLICY

! Verification
Router# show policy-map control-plane
```

---

## 3. 802.1X & Identity Services

### 802.1X Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    802.1X Components                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Supplicant          Authenticator        Auth Server     │
│   (Client)            (Switch/WLC)         (ISE/RADIUS)    │
│                                                             │
│   ┌────────┐          ┌────────┐          ┌────────┐       │
│   │  PC    │──EAPOL──▶│ Switch │──RADIUS─▶│  ISE   │       │
│   │(802.1X │          │        │          │        │       │
│   │ client)│◀─────────│        │◀─────────│        │       │
│   └────────┘          └────────┘          └────────┘       │
│                                                             │
│   Flow:                                                     │
│   1. Client connects (port unauthorized)                   │
│   2. Switch sends EAP-Request/Identity                     │
│   3. Client responds with identity                         │
│   4. Switch forwards to RADIUS                             │
│   5. RADIUS challenges client                              │
│   6. Client provides credentials                           │
│   7. RADIUS validates, returns Access-Accept               │
│   8. Switch authorizes port, applies policy                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 802.1X Switch Configuration

```cisco
! Enable AAA
Switch(config)# aaa new-model
Switch(config)# aaa authentication dot1x default group radius
Switch(config)# aaa authorization network default group radius
Switch(config)# aaa accounting dot1x default start-stop group radius

! Configure RADIUS server
Switch(config)# radius server ISE-PRIMARY
Switch(config-radius-server)# address ipv4 10.1.1.100 auth-port 1812 acct-port 1813
Switch(config-radius-server)# key RadiusSecret123

! Enable 802.1X globally
Switch(config)# dot1x system-auth-control

! Configure interface
Switch(config)# interface GigabitEthernet0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
Switch(config-if)# authentication port-control auto
Switch(config-if)# authentication host-mode multi-auth
Switch(config-if)# dot1x pae authenticator
Switch(config-if)# mab                              ! MAB fallback
Switch(config-if)# authentication order dot1x mab
Switch(config-if)# authentication priority dot1x mab

! Verification
Switch# show dot1x all
Switch# show authentication sessions
Switch# show authentication sessions interface gi0/1
```

### MAB (MAC Authentication Bypass)

```
MAB for devices without 802.1X supplicant:
• Printers, IP phones, IoT devices
• Uses MAC address as username/password
• Fallback when 802.1X fails

Authentication Order:
1. dot1x (try 802.1X first)
2. mab (fallback to MAB)
3. webauth (optional web portal)
```

---

## 4. MACsec

### MACsec Overview

```
MACsec (802.1AE) - Layer 2 encryption

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Without MACsec:                                           │
│   ┌────────┐        Plaintext         ┌────────┐           │
│   │Switch A│━━━━━━━━━━━━━━━━━━━━━━━━━│Switch B│           │
│   └────────┘  (sniffable, tamper)     └────────┘           │
│                                                             │
│   With MACsec:                                              │
│   ┌────────┐       Encrypted          ┌────────┐           │
│   │Switch A│═══════════════════════════│Switch B│           │
│   └────────┘  (AES-GCM-128/256)       └────────┘           │
│                                                             │
│   Benefits:                                                 │
│   • Confidentiality (encryption)                           │
│   • Integrity (ICV - Integrity Check Value)               │
│   • Anti-replay protection                                 │
│   • Line-rate encryption (hardware)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### MACsec Configuration (Switch-to-Switch)

```cisco
! Define key chain
Switch(config)# key chain MACSEC-KEYS macsec
Switch(config-keychain)# key 1
Switch(config-keychain-key)# cryptographic-algorithm aes-256-cmac
Switch(config-keychain-key)# key-string SecretKey123

! Define MKA policy
Switch(config)# mka policy MKA-POLICY
Switch(config-mka-policy)# macsec-cipher-suite gcm-aes-256

! Apply to interface
Switch(config)# interface GigabitEthernet0/1
Switch(config-if)# mka policy MKA-POLICY
Switch(config-if)# mka pre-shared-key key-chain MACSEC-KEYS
Switch(config-if)# macsec

! Verification
Switch# show mka sessions
Switch# show mka statistics
Switch# show macsec interface gi0/1
```

---

## 5. TrustSec & SGT

### TrustSec Overview

```
TrustSec: Policy based on identity, not IP address

Traditional ACL:                 TrustSec SGT:
permit ip 10.1.1.0 any          permit SGT-Employees to SGT-Servers
(What if user moves?)           (Identity follows user)

┌─────────────────────────────────────────────────────────────┐
│                    TrustSec Components                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SGT (Scalable Group Tag):                                 │
│  • 16-bit tag assigned to traffic                         │
│  • Identifies security group (role)                        │
│  • Travels with packet through network                     │
│                                                             │
│  Classification:                                            │
│  • Static (interface/VLAN)                                 │
│  • Dynamic (802.1X/ISE)                                    │
│                                                             │
│  Enforcement:                                               │
│  • SGACL (SGT-based ACL)                                   │
│  • Applied at egress                                       │
│                                                             │
│  Example:                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ Employee │───▶│  Switch  │───▶│  Server  │             │
│  │ SGT=10   │    │ (SGT     │    │ SGT=20   │             │
│  │          │    │  enforced)│    │          │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│                                                             │
│  SGACL: permit-10-to-20 (allow Employee to Server)        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### TrustSec Configuration

```cisco
! Enable CTS (Cisco TrustSec)
Switch(config)# cts authorization list CTS-LIST
Switch(config)# aaa authorization network CTS-LIST group radius

! Static SGT assignment (manual)
Switch(config)# interface GigabitEthernet0/1
Switch(config-if)# cts manual
Switch(config-if-cts-manual)# policy static sgt 10

! VLAN-to-SGT mapping
Switch(config)# cts role-based sgt-map vlan-list 100 sgt 10

! IP-to-SGT mapping (static)
Switch(config)# cts role-based sgt-map 10.1.1.0/24 sgt 10

! SGACL definition
Switch(config)# cts role-based permissions from 10 to 20 PERMIT-ALL
Switch(config)# ip access-list role-based PERMIT-ALL
Switch(config-rb-acl)# permit ip

! Enable enforcement
Switch(config)# cts role-based enforcement

! Verification
Switch# show cts interface
Switch# show cts role-based permissions
Switch# show cts role-based counters
```

---

## 📝 Module 5 Exercises

### Exercise 5.1: CoPP
Create a CoPP policy that:
- Allows 256kbps for BGP
- Allows 128kbps for OSPF
- Limits ICMP to 64kbps
- Drops excess default traffic

### Exercise 5.2: 802.1X
Configure a switch port with:
- 802.1X authentication
- MAB fallback
- Guest VLAN for failures

### Exercise 5.3: MACsec
Configure MACsec between two switches:
- AES-256 encryption
- Pre-shared key

---

*Previous: [← Network Assurance](../04-network-assurance/README.md) | Next: [Automation →](../06-automation/README.md)*

