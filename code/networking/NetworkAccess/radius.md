# RADIUS Protocol 📡

> **Remote Authentication Dial-In User Service**

## Overview

RADIUS is the standard protocol for network access authentication. Originally designed for dial-up, it's now used for Wi-Fi, VPN, and wired 802.1X authentication.

## RADIUS Packet Types

| Code | Name | Description |
|------|------|-------------|
| 1 | Access-Request | Client sends credentials |
| 2 | Access-Accept | Authentication successful |
| 3 | Access-Reject | Authentication failed |
| 4 | Accounting-Request | Start/stop/interim accounting |
| 5 | Accounting-Response | Server acknowledges accounting |
| 11 | Access-Challenge | Server requests more info |

## RADIUS Flow

```
Client              NAS (Switch/AP)         RADIUS Server
  │                      │                       │
  │──── Connect ────────►│                       │
  │                      │                       │
  │◄─── EAP-Request ─────│                       │
  │                      │                       │
  │──── EAP-Response ───►│                       │
  │                      │                       │
  │                      │── Access-Request ────►│
  │                      │   (EAP embedded)      │
  │                      │                       │
  │                      │◄── Access-Challenge ──│
  │                      │                       │
  │◄─── EAP-Request ─────│                       │
  │                      │                       │
  │──── EAP-Response ───►│                       │
  │                      │                       │
  │                      │── Access-Request ────►│
  │                      │                       │
  │                      │◄── Access-Accept ─────│
  │                      │    (VLAN, ACL, etc.)  │
  │                      │                       │
  │◄─── EAP-Success ─────│                       │
  │                      │                       │
  │     [Connected]      │                       │
```

---

## FreeRADIUS Setup

### Installation

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install freeradius freeradius-utils

# RHEL/CentOS
sudo yum install freeradius freeradius-utils

# Start service
sudo systemctl start freeradius
sudo systemctl enable freeradius
```

### Configuration Files

```
/etc/freeradius/3.0/
├── radiusd.conf         # Main config
├── clients.conf         # NAS devices (switches, APs)
├── users                # Local users (testing)
├── mods-available/      # Available modules
├── mods-enabled/        # Enabled modules (symlinks)
├── sites-available/     # Virtual servers
└── sites-enabled/       # Enabled sites
```

### Add RADIUS Client (NAS)

```bash
# /etc/freeradius/3.0/clients.conf

client switch1 {
    ipaddr = 192.168.1.10
    secret = SharedSecret123!
    shortname = switch1
    nastype = cisco
}

client wireless_controller {
    ipaddr = 192.168.1.20
    secret = AnotherSecret456!
    shortname = wlc
    nastype = cisco
}

# Subnet of clients
client office_switches {
    ipaddr = 192.168.1.0/24
    secret = OfficeSecret789!
}
```

### Add Test User

```bash
# /etc/freeradius/3.0/users

# Basic user
testuser    Cleartext-Password := "testpass"

# User with VLAN assignment
employee1   Cleartext-Password := "password123"
            Tunnel-Type = VLAN,
            Tunnel-Medium-Type = IEEE-802,
            Tunnel-Private-Group-ID = "100"

# User with specific attributes
admin       Cleartext-Password := "adminpass"
            Service-Type = Administrative-User,
            Cisco-AVPair = "shell:priv-lvl=15"
```

### Test RADIUS

```bash
# Debug mode (foreground)
sudo freeradius -X

# Test authentication
radtest testuser testpass localhost 0 testing123

# Test with specific NAS
radtest employee1 password123 localhost 0 testing123
```

---

## RADIUS with LDAP/Active Directory

### Enable LDAP Module

```bash
# Link LDAP module
sudo ln -s /etc/freeradius/3.0/mods-available/ldap /etc/freeradius/3.0/mods-enabled/
```

### Configure LDAP

```bash
# /etc/freeradius/3.0/mods-available/ldap

ldap {
    server = 'ldap://dc.example.com'
    port = 389
    
    identity = 'CN=radius,OU=Service Accounts,DC=example,DC=com'
    password = 'ServiceAccountPassword'
    
    base_dn = 'DC=example,DC=com'
    
    user {
        base_dn = "OU=Users,${..base_dn}"
        filter = "(sAMAccountName=%{%{Stripped-User-Name}:-%{User-Name}})"
    }
    
    group {
        base_dn = "OU=Groups,${..base_dn}"
        filter = "(objectClass=group)"
        membership_attribute = 'memberOf'
    }
}
```

---

## Common RADIUS Attributes

| Attribute | ID | Description |
|-----------|-----|-------------|
| User-Name | 1 | Username |
| User-Password | 2 | Password (encrypted) |
| NAS-IP-Address | 4 | IP of NAS device |
| NAS-Port | 5 | Physical port number |
| Service-Type | 6 | Type of service requested |
| Framed-IP-Address | 8 | IP to assign to user |
| Filter-Id | 11 | ACL name to apply |
| Session-Timeout | 27 | Max session time |
| Tunnel-Type | 64 | Tunnel type (VLAN) |
| Tunnel-Medium-Type | 65 | Medium (802) |
| Tunnel-Private-Group-ID | 81 | VLAN ID |
| Calling-Station-Id | 31 | Client MAC address |
| Called-Station-Id | 30 | NAS MAC/SSID |

### Vendor-Specific Attributes (VSA)

```bash
# Cisco VSA examples in users file

# Set privilege level
admin   Cleartext-Password := "adminpass"
        Cisco-AVPair = "shell:priv-lvl=15"

# Assign downloadable ACL
guest   Cleartext-Password := "guestpass"
        Cisco-AVPair = "ip:inacl#1=permit tcp any any eq 80",
        Cisco-AVPair = "ip:inacl#2=permit tcp any any eq 443",
        Cisco-AVPair = "ip:inacl#3=deny ip any any"
```

---

## Cisco Switch RADIUS Configuration

```cisco
! Enable AAA
aaa new-model

! Configure RADIUS server
radius server ISE-PRIMARY
 address ipv4 192.168.1.100 auth-port 1812 acct-port 1813
 key SecretKey123!

radius server ISE-SECONDARY
 address ipv4 192.168.1.101 auth-port 1812 acct-port 1813
 key SecretKey123!

! Create server group
aaa group server radius ISE-SERVERS
 server name ISE-PRIMARY
 server name ISE-SECONDARY

! Authentication methods
aaa authentication dot1x default group ISE-SERVERS
aaa authorization network default group ISE-SERVERS
aaa accounting dot1x default start-stop group ISE-SERVERS

! Enable 802.1X globally
dot1x system-auth-control

! Configure interface
interface GigabitEthernet0/1
 switchport mode access
 authentication port-control auto
 dot1x pae authenticator
```

---

## Troubleshooting

```bash
# FreeRADIUS debug mode
sudo freeradius -X

# Test authentication
radtest user password server port secret

# Check logs
tail -f /var/log/freeradius/radius.log

# Packet capture
sudo tcpdump -i any port 1812 or port 1813 -vv
```

---

*Next: [EAP Protocols →](./eap.md)*

