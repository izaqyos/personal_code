# Network Configuration Tools ⚙️

> **ip, ss, netstat, route, ethtool**

## ip command (iproute2)

### Addresses

```bash
# Show all addresses
ip addr show
ip a

# Show specific interface
ip addr show eth0

# Add address
sudo ip addr add 192.168.1.100/24 dev eth0

# Delete address
sudo ip addr del 192.168.1.100/24 dev eth0
```

### Links

```bash
# Show all interfaces
ip link show
ip l

# Bring interface up/down
sudo ip link set eth0 up
sudo ip link set eth0 down

# Set MTU
sudo ip link set eth0 mtu 9000

# Set MAC address
sudo ip link set eth0 address aa:bb:cc:dd:ee:ff
```

### Routes

```bash
# Show routing table
ip route show
ip r

# Add route
sudo ip route add 10.0.0.0/8 via 192.168.1.1
sudo ip route add 10.0.0.0/8 dev eth0

# Delete route
sudo ip route del 10.0.0.0/8

# Add default gateway
sudo ip route add default via 192.168.1.1

# Show route to destination
ip route get 8.8.8.8
```

### Neighbors (ARP)

```bash
# Show ARP table
ip neigh show
ip n

# Add static ARP
sudo ip neigh add 192.168.1.1 lladdr aa:bb:cc:dd:ee:ff dev eth0

# Flush ARP cache
sudo ip neigh flush all
```

## ss (Socket Statistics)

```bash
# All sockets
ss -a

# Listening sockets
ss -l

# TCP sockets
ss -t

# UDP sockets
ss -u

# Show process info
ss -p

# Numeric (no DNS)
ss -n

# Common combinations
ss -tuln          # TCP/UDP listening, numeric
ss -tunap         # All with process info
ss -s             # Summary statistics

# Filter by port
ss -t sport = :22
ss -t dport = :80

# Filter by state
ss -t state established
ss -t state listening
```

## netstat (legacy)

```bash
# Listening ports
netstat -tuln

# All connections
netstat -tuna

# With process info
netstat -tunap

# Routing table
netstat -r

# Interface statistics
netstat -i

# Statistics by protocol
netstat -s
```

## ethtool

```bash
# Show interface info
ethtool eth0

# Show driver info
ethtool -i eth0

# Show statistics
ethtool -S eth0

# Show ring buffer
ethtool -g eth0

# Set speed/duplex
sudo ethtool -s eth0 speed 1000 duplex full autoneg off
```

## Quick Reference

```bash
# What's my IP?
ip addr show | grep inet

# What's listening?
ss -tuln

# What's connected?
ss -tun

# Show routes
ip route

# Show ARP
ip neigh

# Interface stats
ip -s link show eth0
```

---

*Previous: [← Connectivity](./connectivity.md) | Next: [Protocols →](./protocols.md)*

