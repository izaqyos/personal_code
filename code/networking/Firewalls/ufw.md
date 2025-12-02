# ufw (Uncomplicated Firewall) 🔓

> **Simplified firewall for Ubuntu/Debian**

## Basic Commands

```bash
# Status
sudo ufw status
sudo ufw status verbose
sudo ufw status numbered

# Enable/disable
sudo ufw enable
sudo ufw disable

# Reset to defaults
sudo ufw reset

# Set defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

## Allow/Deny Rules

```bash
# By port
sudo ufw allow 22
sudo ufw allow 22/tcp
sudo ufw allow 5000:5100/tcp

# By service name
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# From specific IP
sudo ufw allow from 192.168.1.100
sudo ufw allow from 192.168.1.0/24

# To specific port from IP
sudo ufw allow from 192.168.1.100 to any port 22

# Deny
sudo ufw deny 23
sudo ufw deny from 10.0.0.1

# Reject (with response)
sudo ufw reject 23
```

## Delete Rules

```bash
# By number
sudo ufw status numbered
sudo ufw delete 2

# By rule
sudo ufw delete allow 80
sudo ufw delete allow ssh
```

## Application Profiles

```bash
# List apps
sudo ufw app list

# App info
sudo ufw app info 'Nginx Full'

# Allow app
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
```

## Advanced Rules

```bash
# Specific interface
sudo ufw allow in on eth0 to any port 80

# Rate limiting (SSH brute force protection)
sudo ufw limit ssh

# Logging
sudo ufw logging on
sudo ufw logging medium  # low, medium, high, full
```

## Quick Setup

```bash
# Basic server
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

---

*Previous: [← firewalld](./firewalld.md) | Next: [pf →](./pf.md)*

