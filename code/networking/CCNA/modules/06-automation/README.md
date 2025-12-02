# Module 6: Automation & Programmability 🤖

> **10% of CCNA Exam | Estimated Time: 8-10 hours**

## Module Overview

⚠️ **THIS MODULE IS COMPLETELY NEW** - None of this existed in the old CCNA!

This module covers network automation fundamentals. As an experienced developer [[memory:11642010]], you'll find many concepts familiar from software development.

---

## Table of Contents

1. [Network Automation Benefits](#1-network-automation-benefits)
2. [REST APIs & HTTP](#2-rest-apis--http)
3. [JSON & YAML Data Formats](#3-json--yaml-data-formats)
4. [Configuration Management](#4-configuration-management)
5. [SDN & Controllers](#5-sdn--controllers)
6. [Cisco DNA Center](#6-cisco-dna-center)
7. [Python for Networking](#7-python-for-networking)

---

## 1. Network Automation Benefits

### Traditional vs Automated

```
Traditional (CLI-based):              Automated:
──────────────────────               ────────────
┌─────┐ ┌─────┐ ┌─────┐             ┌─────────────┐
│ R1  │ │ R2  │ │ R3  │             │ Automation  │
└──┬──┘ └──┬──┘ └──┬──┘             │   Tool      │
   │       │       │                 └──────┬──────┘
   │       │       │                        │
   ▼       ▼       ▼                        ▼
 SSH     SSH     SSH              ┌────────────────┐
 ▼       ▼       ▼                │ API/NETCONF/   │
Manual  Manual  Manual            │ RESTCONF       │
config  config  config            └────────────────┘
                                          │
Time: Hours                        ┌──────┼──────┐
Error: High                        ▼      ▼      ▼
                                 ┌───┐  ┌───┐  ┌───┐
                                 │R1 │  │R2 │  │R3 │
                                 └───┘  └───┘  └───┘
                                  Time: Minutes
                                  Error: Low
```

### Automation Benefits

| Benefit | Description |
|---------|-------------|
| Speed | Configure thousands of devices quickly |
| Consistency | Same config applied uniformly |
| Compliance | Ensure standards are met |
| Scalability | Grow without adding staff |
| Reduced Errors | Eliminate typos, mistakes |
| Documentation | Config-as-code, version control |
| Testing | Validate changes before deployment |

### Automation Use Cases

- **Configuration management** - Deploy, backup, restore configs
- **Monitoring** - Collect data, generate alerts
- **Provisioning** - Spin up new devices/services
- **Compliance** - Audit configurations
- **Troubleshooting** - Automated diagnostics
- **Reporting** - Generate dashboards, reports

---

## 2. REST APIs & HTTP

### HTTP Methods (CRUD Operations)

| Method | Operation | Description |
|--------|-----------|-------------|
| GET | Read | Retrieve data |
| POST | Create | Create new resource |
| PUT | Update | Replace entire resource |
| PATCH | Update | Modify part of resource |
| DELETE | Delete | Remove resource |

### HTTP Response Codes

```
┌─────────────────────────────────────────────────────────────┐
│  Code Range  │  Category        │  Examples                 │
├─────────────────────────────────────────────────────────────┤
│  1xx         │  Informational   │  100 Continue             │
│  2xx         │  Success         │  200 OK, 201 Created      │
│  3xx         │  Redirection     │  301 Moved, 304 Not Mod   │
│  4xx         │  Client Error    │  400 Bad Request          │
│              │                  │  401 Unauthorized         │
│              │                  │  403 Forbidden            │
│              │                  │  404 Not Found            │
│  5xx         │  Server Error    │  500 Internal Error       │
│              │                  │  503 Service Unavailable  │
└─────────────────────────────────────────────────────────────┘
```

### REST API Structure

```
Base URL:    https://api.example.com
Endpoint:    /api/v1/devices
Full URL:    https://api.example.com/api/v1/devices/123

HTTP Request:
┌─────────────────────────────────────────────────────────────┐
│ GET /api/v1/devices/123 HTTP/1.1                           │
│ Host: api.example.com                                       │
│ Authorization: Bearer <token>                               │
│ Accept: application/json                                    │
│ Content-Type: application/json                              │
└─────────────────────────────────────────────────────────────┘

HTTP Response:
┌─────────────────────────────────────────────────────────────┐
│ HTTP/1.1 200 OK                                             │
│ Content-Type: application/json                              │
│                                                             │
│ {                                                           │
│   "id": 123,                                                │
│   "hostname": "router1",                                    │
│   "ip": "192.168.1.1"                                       │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

### API Authentication Types

| Type | Description |
|------|-------------|
| Basic Auth | Username:password (Base64) |
| API Key | Static key in header/query |
| Token | JWT, OAuth tokens |
| OAuth 2.0 | Industry standard |

---

## 3. JSON & YAML Data Formats

### JSON (JavaScript Object Notation)

```json
{
  "hostname": "router1",
  "interfaces": [
    {
      "name": "GigabitEthernet0/0",
      "ip_address": "192.168.1.1",
      "subnet_mask": "255.255.255.0",
      "enabled": true
    },
    {
      "name": "GigabitEthernet0/1",
      "ip_address": "10.0.0.1",
      "subnet_mask": "255.255.255.252",
      "enabled": true
    }
  ],
  "routes": [
    {
      "destination": "0.0.0.0/0",
      "next_hop": "10.0.0.2"
    }
  ]
}
```

### JSON Data Types

| Type | Example |
|------|---------|
| String | `"hello"` |
| Number | `42`, `3.14` |
| Boolean | `true`, `false` |
| Null | `null` |
| Array | `[1, 2, 3]` |
| Object | `{"key": "value"}` |

### YAML (YAML Ain't Markup Language)

```yaml
---
hostname: router1
interfaces:
  - name: GigabitEthernet0/0
    ip_address: 192.168.1.1
    subnet_mask: 255.255.255.0
    enabled: true
  - name: GigabitEthernet0/1
    ip_address: 10.0.0.1
    subnet_mask: 255.255.255.252
    enabled: true
routes:
  - destination: 0.0.0.0/0
    next_hop: 10.0.0.2
```

### JSON vs YAML Comparison

| Feature | JSON | YAML |
|---------|------|------|
| Readability | Moderate | High |
| Comments | No | Yes (#) |
| Data types | Limited | Rich |
| Whitespace | Ignored | Significant |
| Used by | APIs | Config files, Ansible |

---

## 4. Configuration Management

### Configuration Management Tools

| Tool | Language | Agentless | Network Support |
|------|----------|-----------|-----------------|
| Ansible | Python/YAML | Yes | Excellent |
| Puppet | Ruby | No (agent) | Good |
| Chef | Ruby | No (agent) | Moderate |
| SaltStack | Python | Both | Good |

### Ansible Basics

```
Ansible Architecture:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Control Node                 Managed Nodes               │
│   ┌─────────────┐              ┌─────┐                     │
│   │   Ansible   │──SSH/API────▶│ R1  │                     │
│   │             │              └─────┘                     │
│   │ Inventory   │              ┌─────┐                     │
│   │ Playbooks   │──SSH/API────▶│ R2  │                     │
│   │ Modules     │              └─────┘                     │
│   └─────────────┘              ┌─────┐                     │
│                    ──SSH/API──▶│ SW1 │                     │
│                                └─────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### Ansible Inventory File

```ini
# inventory.ini
[routers]
router1 ansible_host=192.168.1.1
router2 ansible_host=192.168.1.2

[switches]
switch1 ansible_host=192.168.1.10
switch2 ansible_host=192.168.1.11

[network:children]
routers
switches

[network:vars]
ansible_network_os=ios
ansible_user=admin
ansible_password=secret
ansible_connection=network_cli
```

### Ansible Playbook Example

```yaml
---
- name: Configure network devices
  hosts: routers
  gather_facts: false
  
  tasks:
    - name: Configure hostname
      cisco.ios.ios_config:
        lines:
          - hostname {{ inventory_hostname }}
    
    - name: Configure NTP
      cisco.ios.ios_config:
        lines:
          - ntp server 10.1.1.100
    
    - name: Save configuration
      cisco.ios.ios_config:
        save_when: modified
```

---

## 5. SDN & Controllers

### Traditional vs SDN Architecture

```
Traditional (Distributed):        SDN (Centralized):
┌───────────────────────┐        ┌───────────────────────┐
│      Management       │        │    SDN Controller     │
│        Plane          │        │  ┌─────────────────┐  │
│   (CLI per device)    │        │  │ Control Plane   │  │
└───────────────────────┘        │  │ (Centralized)   │  │
                                 │  └─────────────────┘  │
┌───────┬───────┬───────┐        └──────────┬────────────┘
│ ┌───┐ │ ┌───┐ │ ┌───┐ │                   │
│ │Ctr│ │ │Ctr│ │ │Ctr│ │        ┌──────────┴────────────┐
│ └───┘ │ └───┘ │ └───┘ │        │    Southbound API     │
│ ┌───┐ │ ┌───┐ │ ┌───┐ │        │   (OpenFlow, etc.)    │
│ │Dat│ │ │Dat│ │ │Dat│ │        └──────────┬────────────┘
│ └───┘ │ └───┘ │ └───┘ │                   │
│  R1   │  R2   │  R3   │        ┌──────────┼────────────┐
└───────┴───────┴───────┘        │    ┌───┐ │ ┌───┐      │
                                 │    │Dat│ │ │Dat│      │
Each device independent          │    └───┘ │ └───┘      │
                                 │     R1   │  R2        │
                                 └──────────────────────┘
                                  Data plane only
```

### SDN Planes

| Plane | Function | Location |
|-------|----------|----------|
| Management | User interface, config | Controller |
| Control | Routing decisions, policies | Controller |
| Data | Packet forwarding | Network devices |

### SDN API Types

```
┌─────────────────────────────────────────────────────────────┐
│                       Applications                          │
│                   (Automation, Security)                    │
└────────────────────────────┬────────────────────────────────┘
                             │ Northbound API
                             │ (REST, Python)
┌────────────────────────────┴────────────────────────────────┐
│                      SDN Controller                         │
│              (Cisco DNA Center, OpenDaylight)               │
└────────────────────────────┬────────────────────────────────┘
                             │ Southbound API
                             │ (OpenFlow, NETCONF, RESTCONF)
┌────────────────────────────┴────────────────────────────────┐
│                    Network Infrastructure                    │
│                   (Routers, Switches, APs)                  │
└─────────────────────────────────────────────────────────────┘
```

### Southbound Protocols

| Protocol | Port | Format | Use |
|----------|------|--------|-----|
| NETCONF | 830 (SSH) | XML | Config, state |
| RESTCONF | 443 (HTTPS) | JSON/XML | Modern REST API |
| OpenFlow | 6653 | Binary | Flow programming |
| CLI/SSH | 22 | Text | Legacy access |
| SNMP | 161 | Binary | Monitoring |

---

## 6. Cisco DNA Center

### DNA Center Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Cisco DNA Center                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Intent-Based Networking (IBN)                             │
│  ─────────────────────────────                              │
│  "What" you want, not "how" to do it                       │
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Design    │ │   Policy    │ │  Provision  │          │
│  │ (topology)  │ │   (rules)   │ │  (deploy)   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │  Assurance  │ │  Security   │ │ Automation  │          │
│  │ (analytics) │ │  (TrustSec) │ │   (APIs)    │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### DNA Center Features

| Feature | Description |
|---------|-------------|
| Design | Network topology, sites, settings |
| Policy | Group-based access control |
| Provision | Device onboarding, templates |
| Assurance | Analytics, insights, AI/ML |
| Platform | APIs for integration |

### DNA Center vs Traditional

| Aspect | Traditional | DNA Center |
|--------|-------------|------------|
| Config | CLI per device | Centralized policies |
| Security | ACLs per device | Group-based (TrustSec) |
| Monitoring | SNMP, Syslog | AI-driven analytics |
| Troubleshooting | Manual | Guided remediation |
| Automation | Scripts | Built-in workflows |

---

## 7. Python for Networking

### Why Python for Networking?

- Simple, readable syntax
- Rich library ecosystem
- Cross-platform
- Community support
- Industry standard for automation

### Essential Libraries

| Library | Purpose |
|---------|---------|
| netmiko | SSH to network devices |
| paramiko | Low-level SSH |
| napalm | Multi-vendor abstraction |
| nornir | Automation framework |
| requests | REST API calls |
| jinja2 | Config templates |

### Basic Python Examples

```python
# Example 1: Connect with Netmiko
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "secret",
}

with ConnectHandler(**device) as conn:
    output = conn.send_command("show ip interface brief")
    print(output)
```

```python
# Example 2: REST API call
import requests
import json

url = "https://sandboxdnac.cisco.com/api/v1/network-device"
headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": "your-token-here"
}

response = requests.get(url, headers=headers, verify=False)
devices = response.json()

for device in devices["response"]:
    print(f"Hostname: {device['hostname']}, IP: {device['managementIpAddress']}")
```

```python
# Example 3: Jinja2 Template
from jinja2 import Template

template = Template("""
hostname {{ hostname }}
!
interface {{ interface }}
 ip address {{ ip }} {{ mask }}
 no shutdown
""")

config = template.render(
    hostname="router1",
    interface="GigabitEthernet0/0",
    ip="192.168.1.1",
    mask="255.255.255.0"
)
print(config)
```

### Python Data Structures for Networking

```python
# Device inventory as dictionary
devices = {
    "router1": {
        "ip": "192.168.1.1",
        "type": "cisco_ios",
        "role": "core"
    },
    "router2": {
        "ip": "192.168.1.2",
        "type": "cisco_ios",
        "role": "distribution"
    }
}

# Interface list
interfaces = [
    {"name": "Gi0/0", "ip": "10.0.0.1/30"},
    {"name": "Gi0/1", "ip": "10.0.1.1/30"},
]

# VLAN configuration
vlans = [10, 20, 30, 40]

# Looping through devices
for hostname, details in devices.items():
    print(f"Connecting to {hostname} at {details['ip']}")
```

---

## 📝 Module 6 Exercises

### Exercise 6.1: JSON Parsing
Given this JSON, write Python to extract all interface names:
```json
{"interfaces": [{"name": "Gi0/0"}, {"name": "Gi0/1"}]}
```

### Exercise 6.2: REST API
Use Python requests to:
1. GET device list from API
2. Parse JSON response
3. Print hostname and IP of each device

### Exercise 6.3: Ansible Playbook
Write a playbook that:
1. Configures hostname
2. Sets NTP server
3. Creates a VLAN
4. Saves configuration

### Exercise 6.4: Jinja2 Template
Create a template for:
- Interface configuration
- Accept variables: interface, ip, mask, description

---

## 🔗 Additional Resources

- [Cisco DevNet](https://developer.cisco.com/) - Free labs, sandboxes
- [Ansible Network Modules](https://docs.ansible.com/ansible/latest/network/index.html)
- [NAPALM Documentation](https://napalm.readthedocs.io/)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)

---

*Previous: [← Security](../05-security/README.md) | Back to: [README](../../README.md)*

