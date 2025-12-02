# TACACS+ 🔒

> **Terminal Access Controller Access-Control System Plus**

## Overview

TACACS+ is primarily used for device administration (SSH/console access to routers/switches), while RADIUS is used for network access.

## TACACS+ vs RADIUS

| Feature | TACACS+ | RADIUS |
|---------|---------|--------|
| Protocol | TCP 49 | UDP 1812/1813 |
| Encryption | Full packet | Password only |
| AAA Separation | Yes | Combined |
| Standard | Cisco proprietary | IETF |
| Primary Use | Device admin | Network access |

## Cisco Switch Configuration

### Basic TACACS+ Setup

```cisco
! Enable AAA
aaa new-model

! Configure TACACS+ server
tacacs server ISE-TACACS
 address ipv4 192.168.1.100
 key SecretKey123

! Server group
aaa group server tacacs+ TACACS-SERVERS
 server name ISE-TACACS

! Authentication for login
aaa authentication login default group TACACS-SERVERS local

! Authorization for exec
aaa authorization exec default group TACACS-SERVERS local

! Authorization for commands
aaa authorization commands 15 default group TACACS-SERVERS local

! Accounting
aaa accounting exec default start-stop group TACACS-SERVERS
aaa accounting commands 15 default start-stop group TACACS-SERVERS
```

### Local Fallback

```cisco
! Create local admin for fallback
username admin privilege 15 secret AdminPass123

! Authentication with local fallback
aaa authentication login default group TACACS-SERVERS local
```

## TACACS+ Server (tac_plus)

### Installation

```bash
# Debian/Ubuntu
sudo apt install tacacs+

# Start service
sudo systemctl start tacacs+
```

### Configuration

```bash
# /etc/tacacs+/tac_plus.conf

# Encryption key (must match devices)
key = "SecretKey123"

# Define users
user = admin {
    member = network-admins
    login = cleartext "adminpassword"
}

user = operator {
    member = network-operators
    login = cleartext "operatorpassword"
}

# Define groups
group = network-admins {
    default service = permit
    service = exec {
        priv-lvl = 15
    }
}

group = network-operators {
    default service = permit
    service = exec {
        priv-lvl = 7
    }
    cmd = show {
        permit .*
    }
    cmd = ping {
        permit .*
    }
}
```

## Troubleshooting

```cisco
! Debug TACACS+
debug tacacs
debug tacacs authentication
debug tacacs authorization
debug tacacs accounting

! Test authentication
test aaa group TACACS-SERVERS admin adminpassword legacy
```

---

*Back: [Network Access README](./README.md)*

