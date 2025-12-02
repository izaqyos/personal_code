# Network Access Control (NAC) 🔑

> **Authentication, Authorization, and Access Control for Networks**

## Overview

This section covers protocols and technologies for controlling who and what can access your network.

## AAA Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AAA Framework                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Authentication          Authorization          Accounting                 │
│  ──────────────          ─────────────          ──────────                 │
│  "Who are you?"          "What can you do?"     "What did you do?"         │
│                                                                             │
│  • Username/Password     • Access levels        • Session logging          │
│  • Certificates          • VLAN assignment      • Traffic accounting       │
│  • Tokens/MFA            • ACL application      • Command logging          │
│  • Biometrics            • Time restrictions    • Billing                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Contents

| Topic | File | Description |
|-------|------|-------------|
| RADIUS | [radius.md](./radius.md) | Remote Authentication Dial-In User Service |
| EAP Protocols | [eap.md](./eap.md) | Extensible Authentication Protocol |
| 802.1X | [8021x.md](./8021x.md) | Port-based Network Access Control |
| TACACS+ | [tacacs.md](./tacacs.md) | Terminal Access Controller Access-Control |

## Protocol Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RADIUS vs TACACS+                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Feature          │ RADIUS              │ TACACS+                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Protocol         │ UDP 1812/1813       │ TCP 49                           │
│  Encryption       │ Password only       │ Full packet                      │
│  AAA Separation   │ Combined            │ Separate                         │
│  Standard         │ IETF (RFC 2865)     │ Cisco proprietary                │
│  Primary Use      │ Network access      │ Device administration            │
│  Multiprotocol    │ Yes                 │ Yes                              │
│                                                                             │
│  Use RADIUS for:  User/device network access (Wi-Fi, VPN, 802.1X)         │
│  Use TACACS+ for: Network device administration (SSH to routers)          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 802.1X Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        802.1X Components                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Supplicant           Authenticator          Authentication Server        │
│   (Client)             (Switch/AP)            (RADIUS)                     │
│                                                                             │
│   ┌─────────┐          ┌─────────┐            ┌─────────┐                  │
│   │   PC    │◄──EAP───►│  Switch │◄──RADIUS──►│   ISE   │                  │
│   │ Laptop  │  (EAPOL) │   AP    │            │FreeRADIUS                  │
│   │ Phone   │          │         │            │   NPS   │                  │
│   └─────────┘          └─────────┘            └─────────┘                  │
│                                                                             │
│   Flow:                                                                     │
│   1. Client connects to port (port is unauthorized)                        │
│   2. Switch sends EAP-Request/Identity                                     │
│   3. Client responds with identity                                         │
│   4. Switch forwards to RADIUS server                                      │
│   5. RADIUS challenges (via EAP method)                                    │
│   6. Client responds with credentials                                      │
│   7. RADIUS sends Accept/Reject                                            │
│   8. Switch authorizes/denies port access                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Reference: EAP Methods

| Method | Credentials | Security | Deployment |
|--------|-------------|----------|------------|
| EAP-TLS | Certificates | ★★★★★ | Complex (PKI needed) |
| PEAP | User/pass + server cert | ★★★★☆ | Common |
| EAP-TTLS | User/pass + server cert | ★★★★☆ | Common |
| EAP-FAST | User/pass (PAC) | ★★★☆☆ | Cisco |
| EAP-MD5 | User/pass | ★☆☆☆☆ | Avoid |

---

*Related: [CCNP Security Module](../CCNP/modules/05-security/)*

