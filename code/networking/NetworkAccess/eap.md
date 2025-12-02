# EAP Protocols 🔐

> **Extensible Authentication Protocol Methods**

## Overview

EAP is a framework for authentication, not a specific method. Various EAP methods provide different security levels and credential types.

## EAP Methods Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EAP Methods Overview                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Method      │ Client Cert │ Server Cert │ Credentials │ Security         │
│  ───────────────────────────────────────────────────────────────────────── │
│  EAP-TLS     │ Required    │ Required    │ Certificate │ ★★★★★           │
│  PEAP        │ No          │ Required    │ User/Pass   │ ★★★★☆           │
│  EAP-TTLS    │ No          │ Required    │ User/Pass   │ ★★★★☆           │
│  EAP-FAST    │ No          │ Optional    │ User/Pass   │ ★★★☆☆           │
│  EAP-MD5     │ No          │ No          │ User/Pass   │ ★☆☆☆☆           │
│  LEAP        │ No          │ No          │ User/Pass   │ ★☆☆☆☆ (broken)  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## EAP-TLS (Most Secure)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EAP-TLS Flow                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Client                    Server                                          │
│    │                         │                                             │
│    │◄── EAP-Request/Identity │                                             │
│    │                         │                                             │
│    │── EAP-Response/Identity─►│                                             │
│    │                         │                                             │
│    │◄── EAP-TLS Start ───────│                                             │
│    │                         │                                             │
│    │── Client Hello ─────────►│                                             │
│    │                         │                                             │
│    │◄── Server Hello ────────│                                             │
│    │◄── Server Certificate ──│                                             │
│    │◄── Certificate Request ─│                                             │
│    │                         │                                             │
│    │── Client Certificate ───►│                                             │
│    │── Key Exchange ─────────►│                                             │
│    │── Certificate Verify ───►│                                             │
│    │                         │                                             │
│    │◄── EAP-Success ─────────│                                             │
│                                                                             │
│  Both client and server present certificates                               │
│  Strongest authentication - requires PKI infrastructure                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### FreeRADIUS EAP-TLS Config

```bash
# /etc/freeradius/3.0/mods-available/eap

eap {
    default_eap_type = tls
    
    tls-config tls-common {
        private_key_file = /etc/freeradius/3.0/certs/server.key
        certificate_file = /etc/freeradius/3.0/certs/server.pem
        ca_file = /etc/freeradius/3.0/certs/ca.pem
        
        # Require client certificate
        require_client_cert = yes
    }
    
    tls {
        tls = tls-common
    }
}
```

---

## PEAP (Protected EAP)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            PEAP Flow                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase 1: TLS Tunnel Establishment                                         │
│  ─────────────────────────────────                                          │
│  Client                    Server                                          │
│    │                         │                                             │
│    │◄── Server Certificate ──│  (Client verifies server)                   │
│    │                         │                                             │
│    │═══ TLS Tunnel Created ══│                                             │
│                                                                             │
│  Phase 2: Inner Authentication (inside tunnel)                             │
│  ─────────────────────────────────────────────                              │
│    │                         │                                             │
│    │── Username/Password ────►│  (Protected by TLS tunnel)                 │
│    │   (MSCHAPv2 typically)  │                                             │
│    │                         │                                             │
│    │◄── EAP-Success ─────────│                                             │
│                                                                             │
│  Only server certificate required (no client PKI)                          │
│  Most common enterprise deployment                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### FreeRADIUS PEAP Config

```bash
# /etc/freeradius/3.0/mods-available/eap

eap {
    default_eap_type = peap
    
    tls-config tls-common {
        private_key_file = /etc/freeradius/3.0/certs/server.key
        certificate_file = /etc/freeradius/3.0/certs/server.pem
        ca_file = /etc/freeradius/3.0/certs/ca.pem
    }
    
    peap {
        tls = tls-common
        default_eap_type = mschapv2
        virtual_server = "inner-tunnel"
    }
    
    mschapv2 {
    }
}
```

---

## EAP-TTLS

Similar to PEAP but more flexible inner methods:

```bash
# Supported inner methods:
# - PAP (legacy, requires TLS tunnel)
# - CHAP
# - MS-CHAP
# - MS-CHAPv2
# - EAP (nested)
```

### FreeRADIUS EAP-TTLS Config

```bash
eap {
    default_eap_type = ttls
    
    ttls {
        tls = tls-common
        default_eap_type = md5
        virtual_server = "inner-tunnel"
    }
}
```

---

## EAP-FAST (Cisco)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EAP-FAST Overview                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Uses PAC (Protected Access Credential) instead of certificates            │
│                                                                             │
│  PAC Provisioning:                                                          │
│  • Automatic (in-band) - Initial connection provisions PAC                 │
│  • Manual (out-of-band) - PAC distributed separately                       │
│                                                                             │
│  Phases:                                                                    │
│  1. PAC provisioning (if needed)                                           │
│  2. TLS tunnel using PAC                                                   │
│  3. Inner authentication                                                    │
│                                                                             │
│  Pros: No PKI required, faster than PEAP                                   │
│  Cons: Cisco proprietary, less secure than EAP-TLS                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Client Configuration

### Windows (PEAP)

```
1. Open Network settings
2. Select Wi-Fi network > Properties
3. Security tab:
   - Security type: WPA2-Enterprise
   - Encryption: AES
   - Authentication: Microsoft PEAP
4. Settings:
   - Validate server certificate: Yes
   - Connect to servers: radius.example.com
   - Trusted Root CA: Your CA
   - Authentication method: EAP-MSCHAPv2
```

### Linux (wpa_supplicant)

```bash
# /etc/wpa_supplicant/wpa_supplicant.conf

# PEAP-MSCHAPv2
network={
    ssid="Corporate-WiFi"
    key_mgmt=WPA-EAP
    eap=PEAP
    identity="username"
    password="password"
    ca_cert="/etc/ssl/certs/ca.pem"
    phase2="auth=MSCHAPV2"
}

# EAP-TLS
network={
    ssid="Secure-WiFi"
    key_mgmt=WPA-EAP
    eap=TLS
    identity="user@example.com"
    ca_cert="/etc/ssl/certs/ca.pem"
    client_cert="/etc/ssl/certs/user.pem"
    private_key="/etc/ssl/private/user.key"
    private_key_passwd="keypassword"
}
```

---

## Security Recommendations

| Scenario | Recommended Method |
|----------|-------------------|
| High security, PKI exists | EAP-TLS |
| Enterprise, no PKI | PEAP-MSCHAPv2 |
| Guest access | Captive portal (no EAP) |
| IoT devices | MAB (MAC Auth Bypass) |
| Legacy compatibility | EAP-TTLS |

---

*Previous: [← RADIUS](./radius.md) | Next: [802.1X →](./8021x.md)*

