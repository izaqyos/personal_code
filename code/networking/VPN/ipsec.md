# IPsec VPN Deep Dive 🔒

> **Industry standard for secure site-to-site and remote access VPNs**

## IPsec Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           IPsec Framework                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    IKE (Internet Key Exchange)                       │   │
│  │              Establishes secure channel, negotiates keys             │   │
│  │                                                                      │   │
│  │    Phase 1 (IKE SA)          │     Phase 2 (IPsec SA)               │   │
│  │    ─────────────────         │     ──────────────────               │   │
│  │    • Authentication          │     • Negotiates IPsec params        │   │
│  │    • DH key exchange         │     • Creates IPsec SA pair          │   │
│  │    • Creates IKE SA          │     • Quick Mode                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    IPsec Protocols                                   │   │
│  │                                                                      │   │
│  │    ESP (Encapsulating Security Payload)    AH (Auth Header)         │   │
│  │    ──────────────────────────────────      ────────────────         │   │
│  │    • Encryption + Authentication           • Authentication only    │   │
│  │    • Protocol 50                           • Protocol 51            │   │
│  │    • Most common                           • Rarely used            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Modes                                             │   │
│  │                                                                      │   │
│  │    Transport Mode              │     Tunnel Mode                    │   │
│  │    ──────────────              │     ───────────                    │   │
│  │    Original IP header kept     │     New IP header added            │   │
│  │    Host-to-host                │     Site-to-site (most common)     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## IKEv1 vs IKEv2

| Feature | IKEv1 | IKEv2 |
|---------|-------|-------|
| Messages to establish | 6 (Main) or 3 (Aggressive) | 4 |
| NAT Traversal | Add-on | Built-in |
| EAP Support | No | Yes |
| MOBIKE | No | Yes (mobility) |
| Reliability | No | Built-in |
| Recommendation | Legacy | **Use this** |

## Encryption & Integrity Algorithms

### Encryption (Confidentiality)

| Algorithm | Key Size | Security | Recommendation |
|-----------|----------|----------|----------------|
| DES | 56-bit | ❌ Broken | Never use |
| 3DES | 168-bit | ⚠️ Weak | Avoid |
| AES-128 | 128-bit | ✅ Good | Acceptable |
| AES-256 | 256-bit | ✅ Strong | **Recommended** |
| ChaCha20 | 256-bit | ✅ Strong | Mobile/embedded |

### Integrity (Hash/HMAC)

| Algorithm | Output | Security | Recommendation |
|-----------|--------|----------|----------------|
| MD5 | 128-bit | ❌ Broken | Never use |
| SHA-1 | 160-bit | ⚠️ Weak | Avoid |
| SHA-256 | 256-bit | ✅ Good | **Recommended** |
| SHA-384 | 384-bit | ✅ Strong | High security |
| SHA-512 | 512-bit | ✅ Strong | High security |

### Diffie-Hellman Groups

| Group | Type | Size | Recommendation |
|-------|------|------|----------------|
| 1 | MODP | 768-bit | ❌ Never |
| 2 | MODP | 1024-bit | ❌ Never |
| 5 | MODP | 1536-bit | ⚠️ Avoid |
| 14 | MODP | 2048-bit | ✅ Minimum |
| 19 | ECP | 256-bit | ✅ Good |
| 20 | ECP | 384-bit | ✅ **Recommended** |
| 21 | ECP | 521-bit | ✅ High security |

---

## Linux IPsec with strongSwan

### Installation

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install strongswan strongswan-pki libcharon-extra-plugins

# RHEL/CentOS
sudo yum install epel-release
sudo yum install strongswan
```

### Site-to-Site Configuration

**Site A: 192.168.1.0/24 ↔ Site B: 192.168.2.0/24**

```bash
# /etc/ipsec.conf (Site A)
config setup
    charondebug="ike 2, knl 2, cfg 2"

conn site-to-site
    type=tunnel
    auto=start
    keyexchange=ikev2
    
    # Authentication
    authby=secret
    
    # Encryption
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256!
    
    # Site A (local)
    left=203.0.113.1
    leftsubnet=192.168.1.0/24
    leftid=@site-a.example.com
    
    # Site B (remote)
    right=198.51.100.1
    rightsubnet=192.168.2.0/24
    rightid=@site-b.example.com
    
    # Options
    dpdaction=restart
    dpddelay=30s
```

```bash
# /etc/ipsec.secrets
@site-a.example.com @site-b.example.com : PSK "SuperSecretKey123!"
```

### Road Warrior (Remote Access) Configuration

```bash
# /etc/ipsec.conf (Server)
config setup
    uniqueids=never

conn roadwarrior
    type=tunnel
    auto=add
    keyexchange=ikev2
    
    # Server
    left=%any
    leftsubnet=0.0.0.0/0
    leftcert=server-cert.pem
    leftid=@vpn.example.com
    leftsendcert=always
    
    # Clients
    right=%any
    rightid=%any
    rightauth=eap-mschapv2
    rightsourceip=10.10.10.0/24
    rightdns=8.8.8.8,8.8.4.4
    
    eap_identity=%identity
    dpdaction=clear
    fragmentation=yes
```

### strongSwan Commands

```bash
# Start/stop
sudo systemctl start strongswan
sudo systemctl enable strongswan

# Connection management
sudo ipsec up site-to-site
sudo ipsec down site-to-site
sudo ipsec restart

# Status and debugging
sudo ipsec status
sudo ipsec statusall
sudo ipsec listcerts
sudo ipsec listcacerts

# Logs
sudo journalctl -u strongswan -f
```

---

## Cisco IOS IPsec Configuration

### IKEv2 Site-to-Site

```cisco
! Step 1: IKEv2 Proposal
crypto ikev2 proposal IKEV2-PROP
 encryption aes-cbc-256
 integrity sha384
 group 20

! Step 2: IKEv2 Policy
crypto ikev2 policy IKEV2-POL
 proposal IKEV2-PROP

! Step 3: IKEv2 Keyring
crypto ikev2 keyring KEYRING
 peer REMOTE-SITE
  address 198.51.100.1
  pre-shared-key S3cr3tK3y!

! Step 4: IKEv2 Profile
crypto ikev2 profile IKEV2-PROF
 match identity remote address 198.51.100.1
 authentication remote pre-share
 authentication local pre-share
 keyring local KEYRING

! Step 5: IPsec Transform Set
crypto ipsec transform-set TSET esp-aes 256 esp-sha384-hmac
 mode tunnel

! Step 6: IPsec Profile
crypto ipsec profile IPSEC-PROF
 set transform-set TSET
 set ikev2-profile IKEV2-PROF

! Step 7: Tunnel Interface
interface Tunnel0
 ip address 10.0.0.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 198.51.100.1
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile IPSEC-PROF

! Step 8: Routing
ip route 192.168.2.0 255.255.255.0 Tunnel0
```

### Verification Commands

```cisco
show crypto ikev2 sa
show crypto ikev2 sa detailed
show crypto ipsec sa
show crypto session
show crypto session detail
debug crypto ikev2
debug crypto ipsec
```

---

## IPsec Packet Structure

### ESP Tunnel Mode

```
Original Packet:
┌──────────────┬─────────────────────────────────┐
│   IP Header  │          Payload                │
│  (Original)  │                                 │
└──────────────┴─────────────────────────────────┘

After ESP Tunnel Encapsulation:
┌──────────────┬──────────────┬──────────────┬─────────────────────────────────┬──────────────┬──────────────┐
│  New IP Hdr  │   ESP Hdr    │ Original IP  │        Original Payload         │  ESP Trailer │   ESP Auth   │
│  (Tunnel)    │ SPI + Seq#   │   Header     │                                 │  Pad + NH    │     ICV      │
└──────────────┴──────────────┴──────────────┴─────────────────────────────────┴──────────────┴──────────────┘
                              └────────────────────── Encrypted ────────────────────────────────┘
               └────────────────────────────────────── Authenticated ───────────────────────────────────────────┘
```

---

## NAT Traversal (NAT-T)

```
Problem: ESP (Protocol 50) can't traverse NAT

Solution: NAT-T encapsulates ESP in UDP 4500

Normal IPsec:
┌──────────────┬──────────────┬─────────────────────┐
│   IP Header  │   ESP Hdr    │   Encrypted Data    │
│              │ Protocol 50  │                     │
└──────────────┴──────────────┴─────────────────────┘
                    ↓
                 NAT breaks this!

With NAT-T:
┌──────────────┬──────────────┬──────────────┬─────────────────────┐
│   IP Header  │  UDP Header  │   ESP Hdr    │   Encrypted Data    │
│              │  Port 4500   │              │                     │
└──────────────┴──────────────┴──────────────┴─────────────────────┘
                    ↓
                NAT can modify UDP headers - works!
```

---

## Troubleshooting IPsec

### Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Phase 1 fails | Mismatched proposal | Check IKE params |
| Phase 2 fails | Mismatched transform | Check ESP params |
| Tunnel up, no traffic | Missing routes | Check routing |
| Intermittent drops | DPD timeouts | Adjust DPD settings |
| NAT issues | NAT-T not enabled | Enable UDP 4500 |

### Debugging Steps

```bash
# Linux (strongSwan)
sudo swanctl --log
sudo tcpdump -i any port 500 or port 4500

# Check SA status
sudo swanctl --list-sas
sudo swanctl --list-conns

# Packet capture
sudo tcpdump -i eth0 esp or udp port 500 or udp port 4500 -w ipsec.pcap
```

---

## Security Best Practices

1. **Use IKEv2** - Don't use IKEv1 for new deployments
2. **AES-256 + SHA-256 minimum** - Avoid weak algorithms
3. **DH Group 20+** - Use elliptic curve groups
4. **Use certificates** - Better than PSK for large deployments
5. **Enable PFS** - Perfect Forward Secrecy
6. **Implement DPD** - Dead Peer Detection
7. **Regular key rotation** - Limit SA lifetimes

---

*Next: [OpenVPN →](./openvpn.md)*

