# nftables 🔥

> **Modern Linux firewall (replaces iptables)**

## Why nftables?

- Single tool for IPv4, IPv6, ARP, bridges
- Better syntax and performance
- Atomic rule updates
- Built-in sets and maps
- Native support in kernel 3.13+

## Basic Commands

```bash
# List all rules
sudo nft list ruleset

# List specific table
sudo nft list table inet filter

# Flush all rules
sudo nft flush ruleset

# Load from file
sudo nft -f /etc/nftables.conf
```

## Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      nftables Hierarchy                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Families:  ip (IPv4), ip6 (IPv6), inet (both), arp, bridge, netdev       │
│                                                                             │
│  Table     →    Chain    →    Rule                                         │
│  (container)    (hook)        (match + action)                             │
│                                                                             │
│  Example:                                                                   │
│  table inet filter {                                                        │
│      chain input {                                                          │
│          type filter hook input priority 0;                                │
│          tcp dport 22 accept                                               │
│      }                                                                      │
│  }                                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Creating Rules

### Create Table and Chain

```bash
# Create table
sudo nft add table inet filter

# Create chain with hook
sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
sudo nft add chain inet filter forward { type filter hook forward priority 0 \; policy drop \; }
sudo nft add chain inet filter output { type filter hook output priority 0 \; policy accept \; }
```

### Add Rules

```bash
# Accept established
sudo nft add rule inet filter input ct state established,related accept

# Accept loopback
sudo nft add rule inet filter input iif lo accept

# Accept SSH
sudo nft add rule inet filter input tcp dport 22 accept

# Accept HTTP/HTTPS
sudo nft add rule inet filter input tcp dport { 80, 443 } accept

# Accept ICMP
sudo nft add rule inet filter input icmp type echo-request accept
sudo nft add rule inet filter input icmpv6 type echo-request accept

# Log and drop
sudo nft add rule inet filter input log prefix \"DROP: \" drop
```

### Delete Rules

```bash
# List with handles
sudo nft -a list table inet filter

# Delete by handle
sudo nft delete rule inet filter input handle 5
```

---

## Configuration File

```bash
#!/usr/sbin/nft -f
# /etc/nftables.conf

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        
        # Connection tracking
        ct state invalid drop
        ct state established,related accept
        
        # Loopback
        iif lo accept
        
        # ICMP
        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept
        
        # SSH
        tcp dport 22 accept
        
        # HTTP/HTTPS
        tcp dport { 80, 443 } accept
        
        # Log dropped
        log prefix "nft-drop: " flags all
    }
    
    chain forward {
        type filter hook forward priority 0; policy drop;
        ct state established,related accept
    }
    
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

## NAT Configuration

```bash
table ip nat {
    chain prerouting {
        type nat hook prerouting priority -100;
        
        # Port forwarding
        tcp dport 8080 dnat to 192.168.1.100:80
    }
    
    chain postrouting {
        type nat hook postrouting priority 100;
        
        # Masquerade
        oif eth0 masquerade
        
        # SNAT
        # ip saddr 192.168.1.0/24 oif eth0 snat to 203.0.113.1
    }
}
```

## Sets and Maps

```bash
# Named set
table inet filter {
    set blocked_ips {
        type ipv4_addr
        elements = { 10.0.0.1, 10.0.0.2 }
    }
    
    set allowed_ports {
        type inet_service
        elements = { 22, 80, 443 }
    }
    
    chain input {
        type filter hook input priority 0;
        ip saddr @blocked_ips drop
        tcp dport @allowed_ports accept
    }
}

# Add to set dynamically
sudo nft add element inet filter blocked_ips { 10.0.0.3 }

# Verdict map (port → action)
table inet filter {
    map port_verdict {
        type inet_service : verdict
        elements = { 22 : accept, 80 : accept, 443 : accept }
    }
    
    chain input {
        tcp dport vmap @port_verdict
    }
}
```

## Rate Limiting

```bash
table inet filter {
    chain input {
        type filter hook input priority 0;
        
        # Limit SSH to 3/minute per IP
        tcp dport 22 ct state new limit rate over 3/minute burst 5 packets drop
        tcp dport 22 accept
        
        # Limit ICMP
        icmp type echo-request limit rate 1/second accept
    }
}
```

---

## iptables to nftables Translation

```bash
# Translate single command
iptables-translate -A INPUT -p tcp --dport 22 -j ACCEPT
# Output: nft add rule ip filter INPUT tcp dport 22 counter accept

# Translate entire ruleset
iptables-save > rules.txt
iptables-restore-translate -f rules.txt > nft-rules.nft
```

## Quick Reference

| iptables | nftables |
|----------|----------|
| `iptables -L` | `nft list ruleset` |
| `iptables -F` | `nft flush ruleset` |
| `-p tcp --dport 22` | `tcp dport 22` |
| `-s 192.168.1.0/24` | `ip saddr 192.168.1.0/24` |
| `-j ACCEPT` | `accept` |
| `-j DROP` | `drop` |
| `-m conntrack --ctstate` | `ct state` |

---

*Previous: [← iptables](./iptables.md) | Next: [firewalld →](./firewalld.md)*

