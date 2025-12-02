# tcpdump Packet Capture 📦

> **Command-line packet analyzer**

## Basic Usage

```bash
# Capture on interface
sudo tcpdump -i eth0

# Capture on all interfaces
sudo tcpdump -i any

# Limit packet count
sudo tcpdump -c 100 -i eth0

# Don't resolve hostnames (faster)
sudo tcpdump -n -i eth0

# Don't resolve hostnames or ports
sudo tcpdump -nn -i eth0

# Verbose output
sudo tcpdump -v -i eth0
sudo tcpdump -vv -i eth0
sudo tcpdump -vvv -i eth0
```

## Filtering

### By Host

```bash
sudo tcpdump host 192.168.1.1
sudo tcpdump src host 192.168.1.1
sudo tcpdump dst host 192.168.1.1
sudo tcpdump host 192.168.1.1 or host 192.168.1.2
```

### By Network

```bash
sudo tcpdump net 192.168.1.0/24
sudo tcpdump src net 10.0.0.0/8
```

### By Port

```bash
sudo tcpdump port 80
sudo tcpdump src port 443
sudo tcpdump dst port 22
sudo tcpdump portrange 1-1024
sudo tcpdump port 80 or port 443
```

### By Protocol

```bash
sudo tcpdump icmp
sudo tcpdump tcp
sudo tcpdump udp
sudo tcpdump arp
sudo tcpdump ip6
```

### Combined Filters

```bash
# HTTP traffic to specific host
sudo tcpdump -i eth0 'host 192.168.1.1 and port 80'

# SSH from specific network
sudo tcpdump 'src net 10.0.0.0/8 and dst port 22'

# DNS queries
sudo tcpdump -i eth0 'udp port 53'

# Not SSH (exclude noise)
sudo tcpdump 'not port 22'

# Complex filter
sudo tcpdump 'tcp and (port 80 or port 443) and host 192.168.1.1'
```

## Output Options

```bash
# Save to file
sudo tcpdump -w capture.pcap -i eth0

# Read from file
tcpdump -r capture.pcap

# Rotate files (100MB each, keep 10)
sudo tcpdump -w capture.pcap -C 100 -W 10 -i eth0

# Timestamp formats
sudo tcpdump -tttt -i eth0    # Human readable
sudo tcpdump -ttttt -i eth0   # Delta from previous

# Show packet contents (hex + ASCII)
sudo tcpdump -X -i eth0

# ASCII only
sudo tcpdump -A -i eth0

# Show link-layer header
sudo tcpdump -e -i eth0

# Snapshot length
sudo tcpdump -s 0 -i eth0     # Full packet
sudo tcpdump -s 96 -i eth0    # First 96 bytes
```

## Common Captures

```bash
# HTTP requests
sudo tcpdump -A -s0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# DNS queries
sudo tcpdump -i eth0 udp port 53

# ICMP (ping)
sudo tcpdump -i eth0 icmp

# SYN packets (new connections)
sudo tcpdump 'tcp[tcpflags] & (tcp-syn) != 0'

# SYN-ACK packets
sudo tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-ack) == (tcp-syn|tcp-ack)'

# RST packets
sudo tcpdump 'tcp[tcpflags] & (tcp-rst) != 0'

# HTTPS (just headers, encrypted)
sudo tcpdump -i eth0 port 443

# ARP
sudo tcpdump -i eth0 arp

# DHCP
sudo tcpdump -i eth0 port 67 or port 68

# VPN traffic
sudo tcpdump -i eth0 'port 500 or port 4500 or esp'
```

## Quick Reference

```bash
# Standard capture to file
sudo tcpdump -nn -i eth0 -w capture.pcap

# Read and filter saved capture
tcpdump -nn -r capture.pcap 'port 80'

# Live monitoring with readable output
sudo tcpdump -nn -i eth0 -A port 80

# Count packets by type
sudo tcpdump -nn -i eth0 | awk '{print $3}' | sort | uniq -c
```

---

*Previous: [← nmap](./nmap.md) | Next: [Wireshark →](./wireshark.md)*

