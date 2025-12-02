# firewalld 🛡️

> **Dynamic firewall manager (RHEL/Fedora/CentOS)**

## Overview

firewalld provides a frontend to iptables/nftables with zones, services, and runtime vs permanent config.

## Basic Commands

```bash
# Status
sudo firewall-cmd --state
sudo systemctl status firewalld

# Start/stop
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Reload (apply permanent changes)
sudo firewall-cmd --reload

# Complete reload
sudo firewall-cmd --complete-reload
```

## Zones

```bash
# List zones
sudo firewall-cmd --get-zones

# List active zones
sudo firewall-cmd --get-active-zones

# Default zone
sudo firewall-cmd --get-default-zone
sudo firewall-cmd --set-default-zone=public

# Zone info
sudo firewall-cmd --zone=public --list-all
sudo firewall-cmd --list-all-zones

# Assign interface to zone
sudo firewall-cmd --zone=internal --change-interface=eth1 --permanent
```

### Built-in Zones

| Zone | Description |
|------|-------------|
| drop | Drop all, no response |
| block | Reject all incoming |
| public | Public networks (default) |
| external | NAT masquerading |
| dmz | DMZ servers |
| work | Work network |
| home | Home network |
| internal | Internal network |
| trusted | Accept all |

## Services

```bash
# List available services
sudo firewall-cmd --get-services

# List enabled services
sudo firewall-cmd --list-services

# Add service
sudo firewall-cmd --add-service=http
sudo firewall-cmd --add-service=http --permanent

# Remove service
sudo firewall-cmd --remove-service=http --permanent

# Multiple services
sudo firewall-cmd --add-service={http,https,dns} --permanent
```

## Ports

```bash
# List open ports
sudo firewall-cmd --list-ports

# Add port
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --add-port=5000-5100/tcp --permanent

# Remove port
sudo firewall-cmd --remove-port=8080/tcp --permanent
```

## Rich Rules

```bash
# List rich rules
sudo firewall-cmd --list-rich-rules

# Allow from specific IP
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.100" accept' --permanent

# Block IP
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.1" reject' --permanent

# Allow port from subnet
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="3306" protocol="tcp" accept' --permanent

# Rate limiting
sudo firewall-cmd --add-rich-rule='rule service name="ssh" limit value="3/m" accept' --permanent

# Log and drop
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" log prefix="BLOCKED: " level="info" drop' --permanent
```

## Port Forwarding

```bash
# Forward port
sudo firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080 --permanent

# Forward to another host
sudo firewall-cmd --add-forward-port=port=80:proto=tcp:toaddr=192.168.1.100 --permanent
sudo firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=192.168.1.100 --permanent

# Enable masquerading (for NAT)
sudo firewall-cmd --add-masquerade --permanent
```

## Direct Rules (iptables syntax)

```bash
# Add direct rule
sudo firewall-cmd --direct --add-rule ipv4 filter INPUT 0 -p tcp --dport 9999 -j ACCEPT

# List direct rules
sudo firewall-cmd --direct --get-all-rules
```

## Quick Reference

```bash
# Show everything
sudo firewall-cmd --list-all

# Common setup
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload

# Check specific service
sudo firewall-cmd --query-service=ssh
```

---

*Previous: [← nftables](./nftables.md) | Next: [ufw →](./ufw.md)*

