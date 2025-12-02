# Network Protocols 📡

> **NTP, DHCP, ARP utilities**

## NTP (Network Time Protocol)

### Check Time Sync

```bash
# Show NTP status
timedatectl status

# Show NTP servers
timedatectl show-timesync

# chronyc (if using chrony)
chronyc sources
chronyc tracking

# ntpq (if using ntpd)
ntpq -p
```

### Configure NTP

```bash
# /etc/systemd/timesyncd.conf
[Time]
NTP=0.pool.ntp.org 1.pool.ntp.org
FallbackNTP=ntp.ubuntu.com

# Restart
sudo systemctl restart systemd-timesyncd
```

### Manual Time Operations

```bash
# Force sync
sudo timedatectl set-ntp true
sudo chronyc makestep

# Set timezone
sudo timedatectl set-timezone America/New_York
timedatectl list-timezones

# Query NTP server
ntpdate -q pool.ntp.org
```

## DHCP

### Client Operations

```bash
# Release and renew
sudo dhclient -r eth0    # Release
sudo dhclient eth0       # Renew

# Verbose
sudo dhclient -v eth0

# Show lease info
cat /var/lib/dhcp/dhclient.leases

# NetworkManager
nmcli con down eth0 && nmcli con up eth0
```

### DHCP Server (dnsmasq)

```bash
# /etc/dnsmasq.conf
interface=eth0
dhcp-range=192.168.1.100,192.168.1.200,12h
dhcp-option=option:router,192.168.1.1
dhcp-option=option:dns-server,8.8.8.8,8.8.4.4

# Static lease
dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.50,hostname
```

### View DHCP Traffic

```bash
sudo tcpdump -i eth0 port 67 or port 68 -vv
```

## ARP

```bash
# Show ARP table
ip neigh show
arp -a

# Add static entry
sudo arp -s 192.168.1.1 aa:bb:cc:dd:ee:ff
sudo ip neigh add 192.168.1.1 lladdr aa:bb:cc:dd:ee:ff dev eth0

# Delete entry
sudo arp -d 192.168.1.1
sudo ip neigh del 192.168.1.1 dev eth0

# Flush cache
sudo ip neigh flush all

# ARP scan (find devices)
sudo arp-scan -l
sudo arp-scan 192.168.1.0/24
```

### ARP Watch

```bash
# Monitor ARP traffic
sudo tcpdump -i eth0 arp

# Detect ARP spoofing
sudo arpwatch -i eth0
```

## Quick Diagnostics

```bash
# Is time synced?
timedatectl status | grep synchronized

# What's my DHCP server?
grep "dhcp-server" /var/lib/dhcp/dhclient.leases

# Who has this IP?
arping 192.168.1.1

# Find all devices on network
sudo arp-scan -l
```

---

*Previous: [← Network Config](./netconfig.md) | Back: [Tools README](./README.md)*

