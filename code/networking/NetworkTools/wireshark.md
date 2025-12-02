# Wireshark Packet Analysis 🦈

> **GUI-based network protocol analyzer**

## Display Filters

### By Protocol

```
http
dns
tcp
udp
icmp
arp
ssl/tls
dhcp
```

### By Address

```
ip.addr == 192.168.1.1
ip.src == 192.168.1.1
ip.dst == 192.168.1.1
eth.addr == aa:bb:cc:dd:ee:ff
ip.addr == 192.168.1.0/24
```

### By Port

```
tcp.port == 80
tcp.srcport == 443
tcp.dstport == 22
udp.port == 53
tcp.port in {80 443 8080}
```

### Operators

```
# Comparison
ip.addr == 192.168.1.1
tcp.port != 22
frame.len > 1000
frame.len >= 100 and frame.len <= 500

# Logical
http and ip.addr == 192.168.1.1
tcp.port == 80 or tcp.port == 443
not arp
!(tcp.port == 22)

# Contains
http.request.uri contains "login"
frame contains "password"
```

## Common Filters

```
# HTTP requests
http.request

# HTTP responses
http.response

# HTTP errors
http.response.code >= 400

# DNS queries
dns.flags.response == 0

# DNS responses
dns.flags.response == 1

# TCP SYN
tcp.flags.syn == 1 and tcp.flags.ack == 0

# TCP RST
tcp.flags.reset == 1

# TCP retransmissions
tcp.analysis.retransmission

# Slow responses
tcp.time_delta > 0.5

# TLS handshake
tls.handshake
```

## tshark (CLI Wireshark)

```bash
# Basic capture
tshark -i eth0

# With filter
tshark -i eth0 -f "port 80"

# Display filter
tshark -i eth0 -Y "http.request"

# Save capture
tshark -i eth0 -w capture.pcap

# Read capture
tshark -r capture.pcap

# Specific fields
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# Statistics
tshark -r capture.pcap -q -z io,stat,1
tshark -r capture.pcap -q -z conv,tcp
tshark -r capture.pcap -q -z http,tree
```

## Analysis Tips

### Follow Stream
- Right-click packet → Follow → TCP/UDP/HTTP Stream

### Statistics Menu
- Conversations (ip, tcp, udp)
- Endpoints
- Protocol Hierarchy
- IO Graphs

### Coloring Rules
- View → Coloring Rules
- Helps identify issues visually

---

*Previous: [← tcpdump](./tcpdump.md) | Next: [Connectivity →](./connectivity.md)*

