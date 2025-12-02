# Network Tools & Protocols 🛠️

> **Essential tools for network troubleshooting and analysis**

## Overview

This section covers practical network tools every network engineer should master.

## Tool Categories

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Network Tools Overview                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DNS & Resolution          Packet Capture          Scanning & Discovery    │
│  ─────────────────         ──────────────          ────────────────────    │
│  • dig                     • tcpdump               • nmap                  │
│  • nslookup                • Wireshark             • arp-scan              │
│  • host                    • tshark                • netdiscover           │
│  • whois                   • tcpflow               • masscan               │
│                                                                             │
│  Connectivity              Performance             Protocols               │
│  ────────────              ───────────             ─────────               │
│  • ping                    • iperf3                • NTP                   │
│  • traceroute/mtr          • speedtest-cli         • DHCP                  │
│  • telnet/nc               • bmon                  • ARP                   │
│  • curl/wget               • nethogs               • ICMP                  │
│                                                                             │
│  Network Config            Traffic Analysis        Security                │
│  ─────────────             ────────────────        ────────                │
│  • ip / ifconfig           • ntopng                • OpenSSL               │
│  • ss / netstat            • vnstat                • testssl.sh            │
│  • route                   • iftop                 • nikto                 │
│  • ethtool                 • nload                 • hydra                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Contents

| Topic | File | Description |
|-------|------|-------------|
| DNS Tools | [dns.md](./dns.md) | dig, nslookup, host |
| nmap | [nmap.md](./nmap.md) | Network scanner |
| tcpdump | [tcpdump.md](./tcpdump.md) | Packet capture |
| Wireshark | [wireshark.md](./wireshark.md) | GUI packet analysis |
| Connectivity | [connectivity.md](./connectivity.md) | ping, traceroute, mtr |
| Network Config | [netconfig.md](./netconfig.md) | ip, ss, netstat |
| Protocols | [protocols.md](./protocols.md) | NTP, DHCP |

## Quick Reference

### Connectivity Testing

```bash
# Basic connectivity
ping -c 4 8.8.8.8
ping6 -c 4 2001:4860:4860::8888

# Path tracing
traceroute 8.8.8.8
mtr -r 8.8.8.8

# Port testing
nc -zv host.example.com 22
telnet host.example.com 80
```

### DNS Queries

```bash
# Quick lookup
dig example.com
nslookup example.com
host example.com

# Specific record types
dig example.com MX
dig example.com AAAA
dig -x 8.8.8.8  # Reverse lookup
```

### Network Information

```bash
# Interfaces
ip addr show
ip link show

# Routing
ip route show
route -n

# Connections
ss -tuln
netstat -tuln
```

### Packet Capture

```bash
# Quick capture
sudo tcpdump -i eth0
sudo tcpdump -i any port 80

# Save to file
sudo tcpdump -i eth0 -w capture.pcap
```

### Scanning

```bash
# Quick scan
nmap -sn 192.168.1.0/24    # Ping sweep
nmap -p 22,80,443 host     # Port scan
nmap -sV host              # Version detection
```

---

## Installation (Debian/Ubuntu)

```bash
# DNS tools
sudo apt install dnsutils bind9-host whois

# Network tools
sudo apt install net-tools iproute2 iputils-ping traceroute mtr-tiny

# Packet capture
sudo apt install tcpdump wireshark tshark

# Scanning
sudo apt install nmap masscan

# Performance
sudo apt install iperf3 speedtest-cli bmon iftop nethogs
```

---

*Related: [CCNA Fundamentals](../CCNA/modules/01-network-fundamentals/)*

