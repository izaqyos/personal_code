# VPN Troubleshooting Guide 🔧

## General Troubleshooting Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VPN Troubleshooting Flowchart                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Can you reach the VPN server?                                          │
│     └── ping / telnet to VPN port                                          │
│                                                                             │
│  2. Is the tunnel establishing?                                            │
│     └── Check logs, handshake status                                       │
│                                                                             │
│  3. Is traffic flowing through tunnel?                                     │
│     └── Check routes, interface status                                     │
│                                                                             │
│  4. Can you reach resources on the other side?                            │
│     └── Check firewall, NAT, routing                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Diagnostic Commands

```bash
# Check if VPN interface exists
ip link show
ip addr show

# Check routes
ip route show
route -n

# Check connectivity
ping <vpn-gateway>
traceroute <destination>

# Check DNS
nslookup example.com
dig example.com

# Check firewall
sudo iptables -L -v -n
sudo iptables -t nat -L -v -n

# Capture VPN traffic
sudo tcpdump -i any port 500 or port 4500 or port 1194 or port 51820
```

## Protocol-Specific Troubleshooting

### IPsec
```bash
# strongSwan
sudo ipsec statusall
sudo swanctl --list-sas
journalctl -u strongswan -f

# Cisco
show crypto isakmp sa
show crypto ipsec sa
debug crypto isakmp
debug crypto ipsec
```

### OpenVPN
```bash
sudo openvpn --config client.ovpn --verb 6
tail -f /var/log/openvpn.log
```

### WireGuard
```bash
sudo wg show
sudo wg show wg0 latest-handshakes
dmesg | grep wireguard
```

## Common Issues & Solutions

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Connection timeout | Firewall/port blocked | Check firewall rules |
| Auth failed | Wrong credentials/keys | Verify certificates/keys |
| Tunnel up, no traffic | Routing issue | Check routes and NAT |
| Slow performance | MTU issues | Lower MTU, enable fragmentation |
| Intermittent drops | Keepalive/DPD | Adjust keepalive timers |

---

*Back: [VPN README](./README.md)*

