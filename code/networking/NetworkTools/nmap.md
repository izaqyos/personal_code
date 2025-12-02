# nmap Network Scanner 🔎

> **The essential network discovery and security auditing tool**

## Basic Scanning

### Host Discovery

```bash
# Ping scan (no port scan)
nmap -sn 192.168.1.0/24

# List scan (DNS only, no scan)
nmap -sL 192.168.1.0/24

# Skip host discovery (scan anyway)
nmap -Pn 192.168.1.1

# ARP scan (local network)
nmap -PR 192.168.1.0/24

# TCP SYN ping
nmap -PS22,80,443 192.168.1.0/24

# ICMP ping types
nmap -PE 192.168.1.0/24  # Echo
nmap -PP 192.168.1.0/24  # Timestamp
nmap -PM 192.168.1.0/24  # Netmask
```

### Port Scanning

```bash
# Default scan (top 1000 ports)
nmap 192.168.1.1

# Specific ports
nmap -p 22,80,443 192.168.1.1
nmap -p 1-1000 192.168.1.1
nmap -p- 192.168.1.1           # All 65535 ports

# Fast scan (top 100 ports)
nmap -F 192.168.1.1

# Top ports
nmap --top-ports 20 192.168.1.1
```

---

## Scan Types

```bash
# TCP SYN (half-open, default, requires root)
sudo nmap -sS 192.168.1.1

# TCP Connect (full connection, no root needed)
nmap -sT 192.168.1.1

# UDP scan
sudo nmap -sU 192.168.1.1

# Combined TCP + UDP
sudo nmap -sS -sU 192.168.1.1

# TCP ACK (firewall detection)
sudo nmap -sA 192.168.1.1

# TCP Window scan
sudo nmap -sW 192.168.1.1

# TCP Null, FIN, Xmas (IDS evasion)
sudo nmap -sN 192.168.1.1  # Null
sudo nmap -sF 192.168.1.1  # FIN
sudo nmap -sX 192.168.1.1  # Xmas
```

---

## Service & Version Detection

```bash
# Version detection
nmap -sV 192.168.1.1

# Aggressive version detection
nmap -sV --version-intensity 5 192.168.1.1

# OS detection
sudo nmap -O 192.168.1.1

# Aggressive scan (OS, version, scripts, traceroute)
nmap -A 192.168.1.1

# Light version detection
nmap -sV --version-light 192.168.1.1
```

---

## NSE Scripts (Nmap Scripting Engine)

```bash
# Default scripts
nmap -sC 192.168.1.1
nmap --script=default 192.168.1.1

# Specific script
nmap --script=http-title 192.168.1.1

# Script categories
nmap --script=vuln 192.168.1.1      # Vulnerability
nmap --script=safe 192.168.1.1      # Safe scripts
nmap --script=intrusive 192.168.1.1 # May crash services

# Multiple scripts
nmap --script=http-title,http-headers 192.168.1.1

# Script with arguments
nmap --script=http-brute --script-args userdb=users.txt 192.168.1.1

# List available scripts
ls /usr/share/nmap/scripts/
nmap --script-help=http-*
```

### Useful Scripts

```bash
# Web
nmap --script=http-enum 192.168.1.1
nmap --script=http-vuln* 192.168.1.1

# SMB
nmap --script=smb-enum-shares 192.168.1.1
nmap --script=smb-vuln* 192.168.1.1

# SSL/TLS
nmap --script=ssl-enum-ciphers -p 443 192.168.1.1
nmap --script=ssl-heartbleed -p 443 192.168.1.1

# DNS
nmap --script=dns-brute example.com

# SSH
nmap --script=ssh-auth-methods -p 22 192.168.1.1
```

---

## Output Formats

```bash
# Normal output (default)
nmap 192.168.1.1

# Verbose
nmap -v 192.168.1.1
nmap -vv 192.168.1.1

# Save to file
nmap -oN output.txt 192.168.1.1      # Normal
nmap -oX output.xml 192.168.1.1      # XML
nmap -oG output.gnmap 192.168.1.1    # Grepable
nmap -oA output 192.168.1.1          # All formats

# Append to file
nmap --append-output -oN output.txt 192.168.1.1
```

---

## Timing & Performance

```bash
# Timing templates (0=slowest, 5=fastest)
nmap -T0 192.168.1.1  # Paranoid (IDS evasion)
nmap -T1 192.168.1.1  # Sneaky
nmap -T2 192.168.1.1  # Polite
nmap -T3 192.168.1.1  # Normal (default)
nmap -T4 192.168.1.1  # Aggressive
nmap -T5 192.168.1.1  # Insane

# Custom timing
nmap --min-rate 1000 192.168.1.0/24
nmap --max-rate 100 192.168.1.1
nmap --max-retries 2 192.168.1.1
```

---

## Firewall Evasion

```bash
# Fragment packets
nmap -f 192.168.1.1

# Specify MTU
nmap --mtu 24 192.168.1.1

# Decoys
nmap -D RND:10 192.168.1.1
nmap -D 10.0.0.1,10.0.0.2,ME 192.168.1.1

# Source port
nmap --source-port 53 192.168.1.1

# Randomize hosts
nmap --randomize-hosts 192.168.1.0/24

# Spoof MAC
nmap --spoof-mac 0 192.168.1.1       # Random
nmap --spoof-mac Apple 192.168.1.1   # Vendor
```

---

## Common Use Cases

### Quick Network Survey

```bash
nmap -sn -T4 192.168.1.0/24
```

### Full Port Scan with Services

```bash
sudo nmap -sS -sV -p- -T4 192.168.1.1
```

### Vulnerability Assessment

```bash
sudo nmap -sV --script=vuln 192.168.1.1
```

### Web Server Enumeration

```bash
nmap -sV -p 80,443 --script=http-enum,http-title 192.168.1.1
```

### Stealth Scan

```bash
sudo nmap -sS -T2 -f -D RND:5 --source-port 53 192.168.1.1
```

---

## Port States

| State | Meaning |
|-------|---------|
| open | Service accepting connections |
| closed | No service, but reachable |
| filtered | Firewall blocking |
| unfiltered | Reachable but can't determine state |
| open\|filtered | Can't determine if open or filtered |
| closed\|filtered | Can't determine if closed or filtered |

---

## Quick Reference

```bash
# Discovery
nmap -sn 192.168.1.0/24

# Quick scan
nmap -F 192.168.1.1

# Full scan
nmap -p- -sV -sC -T4 192.168.1.1

# UDP scan
sudo nmap -sU --top-ports 100 192.168.1.1

# OS detection
sudo nmap -O 192.168.1.1

# Save all formats
nmap -oA scan_results 192.168.1.1
```

---

*Previous: [← DNS](./dns.md) | Next: [tcpdump →](./tcpdump.md)*

