# iptables 🧱

> **Classic Linux packet filtering**

## Basic Commands

```bash
# List all rules
sudo iptables -L
sudo iptables -L -n -v              # Numeric, verbose
sudo iptables -L -n -v --line-numbers

# List specific table
sudo iptables -t nat -L -n -v
sudo iptables -t mangle -L -n -v

# Flush all rules
sudo iptables -F                    # Flush filter table
sudo iptables -t nat -F             # Flush NAT table
sudo iptables -X                    # Delete user chains

# Set default policy
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
```

## Rule Syntax

```bash
iptables [-t table] COMMAND chain [options] -j target

# Commands
-A  Append rule
-I  Insert rule (at position)
-D  Delete rule
-R  Replace rule
-L  List rules
-F  Flush rules
-N  New chain
-X  Delete chain
-P  Set policy

# Targets
ACCEPT   Allow packet
DROP     Silently discard
REJECT   Reject with response
LOG      Log to syslog
RETURN   Return from chain
SNAT     Source NAT
DNAT     Destination NAT
MASQUERADE  Dynamic SNAT
```

## Matching Options

```bash
# Protocol
-p tcp
-p udp
-p icmp

# Source/Destination
-s 192.168.1.0/24
-d 10.0.0.1

# Interface
-i eth0              # Input interface
-o eth1              # Output interface

# TCP/UDP ports
--dport 80           # Destination port
--sport 1024:65535   # Source port range
--dport 80,443       # Multiple (with -m multiport)

# TCP flags
--tcp-flags SYN,ACK SYN    # SYN set, ACK not set

# Connection state
-m conntrack --ctstate NEW,ESTABLISHED,RELATED

# MAC address
-m mac --mac-source aa:bb:cc:dd:ee:ff

# Limit rate
-m limit --limit 5/min --limit-burst 10

# String match
-m string --string "pattern" --algo bm
```

---

## Common Rulesets

### Basic Server Firewall

```bash
#!/bin/bash
# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow ICMP (ping)
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "IPT-DROP: " --log-level 4
```

### NAT Gateway/Router

```bash
#!/bin/bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Flush
iptables -F
iptables -t nat -F

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Loopback
iptables -A INPUT -i lo -j ACCEPT

# Established
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow internal to external
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

# Masquerade (SNAT)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Port forwarding (DNAT)
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 \
    -j DNAT --to-destination 192.168.1.100:80
iptables -A FORWARD -p tcp -d 192.168.1.100 --dport 80 -j ACCEPT
```

### Rate Limiting

```bash
# Limit SSH connections (prevent brute force)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
    -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
    -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Limit ICMP
iptables -A INPUT -p icmp --icmp-type echo-request \
    -m limit --limit 1/s --limit-burst 4 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

### Block Common Attacks

```bash
# Block invalid packets
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# Block NULL packets
iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP

# Block SYN flood
iptables -A INPUT -p tcp --syn -m limit --limit 1/s --limit-burst 3 -j ACCEPT
iptables -A INPUT -p tcp --syn -j DROP

# Block XMAS packets
iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP

# Block port scanning
iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST \
    -m limit --limit 1/s --limit-burst 2 -j ACCEPT
```

---

## Persistence

### Debian/Ubuntu

```bash
# Save rules
sudo iptables-save > /etc/iptables/rules.v4
sudo ip6tables-save > /etc/iptables/rules.v6

# Install persistence package
sudo apt install iptables-persistent

# Rules auto-loaded from /etc/iptables/rules.v4
```

### RHEL/CentOS

```bash
# Save rules
sudo service iptables save
# or
sudo iptables-save > /etc/sysconfig/iptables

# Enable service
sudo systemctl enable iptables
```

---

## Debugging

```bash
# View packet/byte counters
sudo iptables -L -n -v

# Zero counters
sudo iptables -Z

# Log packets
iptables -A INPUT -j LOG --log-prefix "DEBUG: " --log-level 7
# View: tail -f /var/log/syslog | grep DEBUG

# Trace packets (raw table)
iptables -t raw -A PREROUTING -p tcp --dport 80 -j TRACE
# Enable trace logging
modprobe nf_log_ipv4
sysctl -w net.netfilter.nf_log.2=nf_log_ipv4

# Connection tracking
cat /proc/net/nf_conntrack
conntrack -L
```

---

*Next: [nftables →](./nftables.md)*

