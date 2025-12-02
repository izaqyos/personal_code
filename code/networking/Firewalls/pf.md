# pf (Packet Filter) 🍎

> **BSD/macOS firewall**

## Overview

pf is the default firewall on OpenBSD, FreeBSD, and macOS.

## macOS Commands

```bash
# Check status
sudo pfctl -s info

# Enable/disable
sudo pfctl -e    # Enable
sudo pfctl -d    # Disable

# Load rules
sudo pfctl -f /etc/pf.conf

# Test config (don't load)
sudo pfctl -n -f /etc/pf.conf

# Show rules
sudo pfctl -s rules
sudo pfctl -s nat
sudo pfctl -s state
```

## Basic Configuration

```bash
# /etc/pf.conf

# Macros
ext_if = "en0"
int_if = "en1"
tcp_services = "{ 22, 80, 443 }"

# Tables
table <bruteforce> persist

# Options
set skip on lo0
set block-policy drop

# Normalization
scrub in all

# NAT
nat on $ext_if from $int_if:network to any -> ($ext_if)

# Filtering
block in all
pass out all keep state

# Allow established
pass in quick on $ext_if proto tcp from any to any port $tcp_services flags S/SA keep state

# Block brute force
block in quick from <bruteforce>
pass in on $ext_if proto tcp to any port ssh flags S/SA keep state \
    (max-src-conn 5, max-src-conn-rate 3/30, overload <bruteforce> flush)
```

## Common Rules

```bash
# Allow SSH
pass in on egress proto tcp to port 22

# Allow HTTP/HTTPS
pass in on egress proto tcp to port { 80 443 }

# Allow ICMP
pass inet proto icmp icmp-type echoreq

# Block RFC1918 from external
block in quick on egress from { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 }
```

## Port Forwarding

```bash
# DNAT
rdr on $ext_if proto tcp from any to ($ext_if) port 8080 -> 192.168.1.100 port 80
pass in on $ext_if proto tcp to 192.168.1.100 port 80
```

## Troubleshooting

```bash
# Show states
sudo pfctl -s state

# Show statistics
sudo pfctl -s info

# Clear states
sudo pfctl -F states

# Log (requires pflog interface)
sudo tcpdump -n -e -ttt -i pflog0
```

---

*Previous: [← ufw](./ufw.md) | Back: [Firewalls README](./README.md)*

