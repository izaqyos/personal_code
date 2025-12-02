# UDP (User Datagram Protocol) ⚡

> **Fast, connectionless, unreliable transport**

## UDP Header

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UDP Header (8 bytes)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    0                   1                   2                   3            │
│    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1         │
│   ├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤         │
│   │          Source Port          │        Destination Port        │  0-3   │
│   ├───────────────────────────────┼────────────────────────────────┤        │
│   │            Length             │           Checksum             │  4-7   │
│   └───────────────────────────────┴────────────────────────────────┘        │
│                                                                             │
│   Minimal header - only 8 bytes!                                           │
│   Compare to TCP's 20-60 bytes                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Header Fields

| Field | Size | Description |
|-------|------|-------------|
| Source Port | 16 bits | Sender's port (optional, can be 0) |
| Destination Port | 16 bits | Receiver's port |
| Length | 16 bits | Header + data length (min 8 bytes) |
| Checksum | 16 bits | Optional in IPv4, mandatory in IPv6 |

## UDP Characteristics

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UDP Properties                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✓ Connectionless     - No handshake, just send                            │
│  ✓ No reliability     - No ACKs, no retransmission                         │
│  ✓ No ordering        - Packets may arrive out of order                    │
│  ✓ No flow control    - Sender can overwhelm receiver                      │
│  ✓ No congestion ctrl - Can flood network                                  │
│  ✓ Datagram-oriented  - Message boundaries preserved                       │
│  ✓ Low overhead       - Only 8 bytes header                                │
│  ✓ Fast               - No connection setup delay                          │
│                                                                             │
│  UDP is a thin wrapper over IP                                             │
│  Adds: port multiplexing + optional checksum                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## UDP vs TCP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    When to Use UDP vs TCP                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Use UDP when:                        Use TCP when:                        │
│  ────────────────                     ─────────────                        │
│  • Speed > reliability                • Reliability needed                 │
│  • Real-time matters                  • Order matters                      │
│  • Small messages                     • Large data transfers               │
│  • Can tolerate loss                  • All data must arrive               │
│  • Multicast/broadcast                • Point-to-point                     │
│  • App handles reliability            • Simple application                 │
│                                                                             │
│  UDP examples:                        TCP examples:                        │
│  • DNS queries                        • HTTP/HTTPS                         │
│  • VoIP/video calls                   • Email (SMTP, IMAP)                │
│  • Online gaming                      • File transfers                     │
│  • Live streaming                     • SSH                                │
│  • DHCP, NTP                          • Database connections               │
│  • SNMP                               • Remote desktop                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Datagram Communication

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UDP Communication Model                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  No Connection:                                                            │
│                                                                             │
│  Client                                            Server                   │
│    │                                                  │                     │
│    │──────────── UDP Datagram 1 ─────────────────────►│                     │
│    │                                                  │                     │
│    │◄─────────── UDP Response ────────────────────────│                     │
│    │                                                  │                     │
│    │──────────── UDP Datagram 2 ─────────────────────►│                     │
│    │                                                  │                     │
│    │    (may be lost, duplicated, or reordered)       │                     │
│    │                                                  │                     │
│    │──────────── UDP Datagram 3 ─────────────────────►│                     │
│    │                                                  │                     │
│                                                                             │
│  Each datagram is independent                                              │
│  No state maintained between datagrams                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## UDP Applications

### DNS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DNS over UDP                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Client                                   DNS Server                        │
│    │                                          │                             │
│    │── Query: A record for example.com ──────►│ (UDP port 53)              │
│    │                                          │                             │
│    │◄── Response: 93.184.216.34 ──────────────│                             │
│    │                                          │                             │
│                                                                             │
│  • Single request-response                                                 │
│  • Small messages (< 512 bytes typically)                                  │
│  • Retransmit from application if needed                                   │
│  • Falls back to TCP if response > 512 bytes                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### VoIP/RTP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Voice/Video over UDP                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Why UDP for real-time media:                                              │
│                                                                             │
│  • Latency is critical (< 150ms for voice)                                 │
│  • Lost packet retransmission would be too late                            │
│  • Better to skip than wait                                                │
│  • Jitter buffer handles timing variations                                 │
│                                                                             │
│  Protocol Stack:                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │  Audio/Video Codec (e.g., Opus, H.264)                          │       │
│  ├─────────────────────────────────────────────────────────────────┤       │
│  │  RTP (Real-time Transport Protocol)                             │       │
│  │  - Sequence numbers (detect loss, reorder)                      │       │
│  │  - Timestamps (synchronization)                                 │       │
│  │  - Payload type (codec identification)                          │       │
│  ├─────────────────────────────────────────────────────────────────┤       │
│  │  UDP                                                            │       │
│  ├─────────────────────────────────────────────────────────────────┤       │
│  │  IP                                                             │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Gaming

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Online Gaming                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Game client                               Game server                      │
│    │                                           │                            │
│    │── Position update (UDP) ─────────────────►│                            │
│    │◄─ World state (UDP) ──────────────────────│                            │
│    │── Position update (UDP) ─────────────────►│  30-60 times/sec          │
│    │◄─ World state (UDP) ──────────────────────│                            │
│    │                                           │                            │
│                                                                             │
│  • Frequent small updates                                                  │
│  • Old state is useless (don't retransmit)                                │
│  • Latency = competitive advantage                                         │
│  • Client-side prediction handles loss                                     │
│  • May use TCP for reliable data (chat, inventory)                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Well-Known UDP Ports

| Port | Service |
|------|---------|
| 53 | DNS |
| 67 | DHCP Server |
| 68 | DHCP Client |
| 69 | TFTP |
| 123 | NTP |
| 137-139 | NetBIOS |
| 161 | SNMP |
| 162 | SNMP Trap |
| 500 | IKE (IPsec) |
| 514 | Syslog |
| 1194 | OpenVPN |
| 4500 | IPsec NAT-T |
| 5060 | SIP |
| 51820 | WireGuard |

## UDP-Lite

```
RFC 3828 - Partial checksum coverage

Standard UDP: Checksum covers entire datagram
             Corrupt bit = entire packet dropped

UDP-Lite:    Checksum covers only critical parts
             Useful when partial data is better than none
             (e.g., audio - corrupt sample is okay)
```

## Reliable UDP Protocols

When you need UDP's speed but some reliability:

| Protocol | Use Case |
|----------|----------|
| QUIC | HTTP/3, multiplexed streams |
| DTLS | Datagram TLS (encrypted UDP) |
| SCTP | Multi-streaming (can run over UDP) |
| UDT | High-speed data transfer |
| KCP | Low latency (gaming) |

## Tools

```bash
# Show UDP connections
ss -u
netstat -u
ss -unp  # with process info

# Listen on UDP port
nc -ul 8080

# Send UDP message
echo "test" | nc -u 192.168.1.1 8080

# UDP port scan
nmap -sU -p 53,123,161 192.168.1.1

# Capture UDP traffic
tcpdump -i eth0 udp
tcpdump -i eth0 'udp port 53'

# Wireshark filter
udp.port == 53
udp.length > 512
```

## Checksum Calculation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UDP Checksum                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Pseudo-header (included in checksum, not transmitted):                    │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │              Source IP Address (32 bits)                       │        │
│  ├────────────────────────────────────────────────────────────────┤        │
│  │            Destination IP Address (32 bits)                    │        │
│  ├──────────────────┬─────────────────┬───────────────────────────┤        │
│  │     Zero (8)     │  Protocol (8)   │     UDP Length (16)       │        │
│  └──────────────────┴─────────────────┴───────────────────────────┘        │
│                                                                             │
│  Checksum covers:                                                          │
│  • Pseudo-header                                                           │
│  • UDP header                                                              │
│  • UDP data                                                                │
│                                                                             │
│  IPv4: Checksum optional (0 = not computed)                               │
│  IPv6: Checksum mandatory                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Previous: [← TCP](./tcp.md) | Next: [ICMP →](./icmp.md)*

