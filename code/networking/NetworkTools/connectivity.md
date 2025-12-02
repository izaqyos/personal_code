# Connectivity Tools 🔗

> **ping, traceroute, mtr, netcat**

## ping

```bash
# Basic ping
ping 8.8.8.8
ping google.com

# Count
ping -c 4 8.8.8.8

# Interval
ping -i 0.5 8.8.8.8

# Packet size
ping -s 1000 8.8.8.8

# IPv6
ping6 2001:4860:4860::8888

# Flood ping (root)
sudo ping -f 192.168.1.1

# Don't fragment
ping -M do -s 1472 8.8.8.8
```

## traceroute / tracepath

```bash
# Basic traceroute
traceroute 8.8.8.8

# UDP (default)
traceroute 8.8.8.8

# ICMP
traceroute -I 8.8.8.8

# TCP
traceroute -T -p 80 8.8.8.8

# No DNS resolution
traceroute -n 8.8.8.8

# tracepath (no root needed)
tracepath 8.8.8.8
```

## mtr (My TraceRoute)

Combines ping + traceroute with live stats.

```bash
# Interactive mode
mtr 8.8.8.8

# Report mode
mtr -r 8.8.8.8

# Report with count
mtr -r -c 100 8.8.8.8

# TCP mode
mtr -T -P 443 8.8.8.8

# No DNS
mtr -n 8.8.8.8

# Show both hostnames and IPs
mtr -b 8.8.8.8
```

## netcat (nc)

```bash
# Test port connectivity
nc -zv 192.168.1.1 22
nc -zv 192.168.1.1 20-25

# Listen on port
nc -l 8080

# Send data
echo "test" | nc 192.168.1.1 8080

# Simple chat
# Server: nc -l 1234
# Client: nc server.ip 1234

# Transfer file
# Receiver: nc -l 1234 > file.txt
# Sender: nc server.ip 1234 < file.txt

# UDP mode
nc -u 192.168.1.1 53

# Timeout
nc -w 5 192.168.1.1 22
```

## curl / wget

```bash
# Basic HTTP GET
curl http://example.com
wget http://example.com

# Show headers
curl -I http://example.com

# Follow redirects
curl -L http://example.com

# POST data
curl -X POST -d "data=value" http://example.com

# Download file
curl -O http://example.com/file.zip
wget http://example.com/file.zip

# Test HTTPS
curl -v https://example.com

# Ignore cert errors
curl -k https://self-signed.example.com
```

## Quick Diagnostics

```bash
# Can I reach the internet?
ping -c 1 8.8.8.8

# Is DNS working?
ping -c 1 google.com

# What path does traffic take?
mtr -r -c 10 8.8.8.8

# Is this port open?
nc -zv host 22

# What's my public IP?
curl ifconfig.me
```

---

*Previous: [← Wireshark](./wireshark.md) | Next: [Network Config →](./netconfig.md)*

