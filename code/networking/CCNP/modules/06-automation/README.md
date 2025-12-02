# Module 6: Automation 🤖

> **10% of ENCOR Exam | Estimated Time: 25-35 hours**

## Module Overview

Building on CCNA automation fundamentals with deeper Python, NETCONF/YANG, and model-driven programmability.

---

## Table of Contents

1. [Python for Network Automation](#1-python-for-network-automation)
2. [NETCONF & YANG](#2-netconf--yang)
3. [RESTCONF](#3-restconf)
4. [Ansible Advanced](#4-ansible-advanced)
5. [DNA Center APIs](#5-dna-center-apis)
6. [Embedded Event Manager](#6-embedded-event-manager)

---

## 1. Python for Network Automation

### Essential Libraries

```python
# Network device interaction
from netmiko import ConnectHandler    # SSH to devices
from napalm import get_network_driver  # Multi-vendor abstraction
from nornir import InitNornir          # Automation framework

# API interaction
import requests                        # REST APIs
from ncclient import manager          # NETCONF

# Data handling
import json                           # JSON parsing
import yaml                           # YAML parsing
import xmltodict                      # XML to dict
from jinja2 import Template           # Templates
```

### Netmiko Advanced Usage

```python
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

# Device dictionary
device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "secret",
    "secret": "enable_secret",
}

# Connect and execute
with ConnectHandler(**device) as conn:
    conn.enable()  # Enter enable mode
    
    # Single command
    output = conn.send_command("show ip route")
    
    # Multiple commands
    commands = ["show version", "show ip int brief"]
    for cmd in commands:
        print(conn.send_command(cmd))
    
    # Configuration changes
    config_commands = [
        "interface loopback100",
        "ip address 10.100.100.1 255.255.255.255",
        "description Created by Python"
    ]
    conn.send_config_set(config_commands)
    conn.save_config()

# Parallel execution across multiple devices
def configure_device(device):
    with ConnectHandler(**device) as conn:
        return conn.send_command("show version")

devices = [device1, device2, device3]
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(configure_device, devices))
```

### NAPALM for Multi-Vendor

```python
from napalm import get_network_driver

# Get the driver for Cisco IOS
driver = get_network_driver("ios")

# Connect to device
device = driver(
    hostname="192.168.1.1",
    username="admin",
    password="secret"
)
device.open()

# Get facts (vendor-agnostic)
facts = device.get_facts()
print(f"Hostname: {facts['hostname']}")
print(f"Uptime: {facts['uptime']}")

# Get interfaces
interfaces = device.get_interfaces()
for name, details in interfaces.items():
    print(f"{name}: {'Up' if details['is_up'] else 'Down'}")

# Configuration management
device.load_merge_candidate(filename="new_config.txt")
diff = device.compare_config()
print(diff)

if diff:
    device.commit_config()  # Apply changes
else:
    device.discard_config()  # No changes needed

device.close()
```

---

## 2. NETCONF & YANG

### NETCONF Overview

```
NETCONF (Network Configuration Protocol):
• RFC 6241
• Uses SSH (port 830)
• XML-based RPC
• Transactional (commit/rollback)
• Uses YANG data models

┌─────────────────────────────────────────────────────────────┐
│                    NETCONF Layers                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Content        │ Configuration/State data (XML)          │
│   Operations     │ <get>, <get-config>, <edit-config>, etc │
│   Messages       │ <rpc>, <rpc-reply>, <notification>      │
│   Transport      │ SSH (port 830)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### YANG Data Models

```
YANG: Data modeling language for NETCONF/RESTCONF

Example YANG module structure:
┌─────────────────────────────────────────────────────────────┐
│ module ietf-interfaces {                                    │
│   container interfaces {                                    │
│     list interface {                                        │
│       key "name";                                           │
│       leaf name { type string; }                           │
│       leaf enabled { type boolean; }                       │
│       leaf mtu { type uint32; }                            │
│       container ipv4 {                                      │
│         list address {                                      │
│           key "ip";                                         │
│           leaf ip { type inet:ipv4-address; }             │
│           leaf netmask { type inet:ipv4-address; }        │
│         }                                                   │
│       }                                                     │
│     }                                                       │
│   }                                                         │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

### NETCONF with Python (ncclient)

```python
from ncclient import manager
import xmltodict

# Connect to device
with manager.connect(
    host="192.168.1.1",
    port=830,
    username="admin",
    password="secret",
    hostkey_verify=False,
    device_params={"name": "iosxe"}
) as m:
    
    # Get running configuration
    config = m.get_config(source="running")
    print(config.xml)
    
    # Get specific data using filter
    filter_xml = """
    <filter>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>GigabitEthernet1</name>
            </interface>
        </interfaces>
    </filter>
    """
    result = m.get(filter_xml)
    
    # Edit configuration
    config_xml = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback100</name>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """
    m.edit_config(target="running", config=config_xml)
```

### Enable NETCONF on Cisco IOS-XE

```cisco
Router(config)# netconf-yang
Router(config)# netconf-yang feature candidate-datastore

! Verification
Router# show netconf-yang sessions
Router# show platform software yang-management process
```

---

## 3. RESTCONF

### RESTCONF Overview

```
RESTCONF (RFC 8040):
• REST API for YANG models
• Uses HTTPS
• JSON or XML data format
• Easier than NETCONF for simple operations

URL Structure:
https://<device>/restconf/data/<yang-module>:<container>/<list>=<key>

Example:
https://192.168.1.1/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet1
```

### RESTCONF with Python

```python
import requests
import json

# Disable SSL warnings for lab
requests.packages.urllib3.disable_warnings()

# Device details
device = {
    "host": "192.168.1.1",
    "username": "admin",
    "password": "secret"
}

# Headers
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Base URL
base_url = f"https://{device['host']}/restconf/data"

# GET interfaces
url = f"{base_url}/ietf-interfaces:interfaces"
response = requests.get(
    url,
    auth=(device["username"], device["password"]),
    headers=headers,
    verify=False
)
interfaces = response.json()
print(json.dumps(interfaces, indent=2))

# GET specific interface
url = f"{base_url}/ietf-interfaces:interfaces/interface=GigabitEthernet1"
response = requests.get(url, auth=(device["username"], device["password"]), 
                       headers=headers, verify=False)

# PUT (create/replace) interface
url = f"{base_url}/ietf-interfaces:interfaces/interface=Loopback100"
payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback100",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "10.100.100.1",
                    "netmask": "255.255.255.255"
                }
            ]
        }
    }
}
response = requests.put(
    url,
    auth=(device["username"], device["password"]),
    headers=headers,
    data=json.dumps(payload),
    verify=False
)
print(f"Status: {response.status_code}")

# PATCH (partial update)
patch_payload = {
    "ietf-interfaces:interface": {
        "name": "Loopback100",
        "description": "Updated by RESTCONF"
    }
}
response = requests.patch(
    url,
    auth=(device["username"], device["password"]),
    headers=headers,
    data=json.dumps(patch_payload),
    verify=False
)

# DELETE interface
response = requests.delete(
    url,
    auth=(device["username"], device["password"]),
    headers=headers,
    verify=False
)
```

### Enable RESTCONF on Cisco IOS-XE

```cisco
Router(config)# restconf
Router(config)# ip http secure-server

! Verification
Router# show platform software yang-management process
```

---

## 4. Ansible Advanced

### Ansible Network Automation

```yaml
# inventory.yml
---
all:
  children:
    routers:
      hosts:
        router1:
          ansible_host: 192.168.1.1
        router2:
          ansible_host: 192.168.1.2
      vars:
        ansible_network_os: cisco.ios.ios
        ansible_connection: ansible.netcommon.network_cli
        ansible_user: admin
        ansible_password: secret
        ansible_become: yes
        ansible_become_method: enable
        ansible_become_password: enable_secret
```

### Advanced Playbook

```yaml
# configure_network.yml
---
- name: Configure Network Devices
  hosts: routers
  gather_facts: no
  
  vars:
    interfaces:
      - name: Loopback100
        ip: 10.100.100.1
        mask: 255.255.255.255
      - name: Loopback101
        ip: 10.100.101.1
        mask: 255.255.255.255
  
  tasks:
    - name: Configure interfaces from variable
      cisco.ios.ios_config:
        lines:
          - description Configured by Ansible
          - ip address {{ item.ip }} {{ item.mask }}
        parents: interface {{ item.name }}
      loop: "{{ interfaces }}"
      register: config_result
    
    - name: Configure OSPF
      cisco.ios.ios_config:
        lines:
          - network 10.0.0.0 0.255.255.255 area 0
        parents: router ospf 1
    
    - name: Save configuration
      cisco.ios.ios_config:
        save_when: modified
    
    - name: Get interface status
      cisco.ios.ios_command:
        commands:
          - show ip interface brief
      register: interface_output
    
    - name: Display output
      debug:
        var: interface_output.stdout_lines

    - name: Backup configuration
      cisco.ios.ios_config:
        backup: yes
        backup_options:
          filename: "{{ inventory_hostname }}_backup.cfg"
          dir_path: ./backups/
```

### Jinja2 Templates with Ansible

```jinja2
{# templates/router_config.j2 #}
hostname {{ hostname }}
!
{% for interface in interfaces %}
interface {{ interface.name }}
 description {{ interface.description | default('No description') }}
 ip address {{ interface.ip }} {{ interface.mask }}
 {% if interface.shutdown | default(false) %}
 shutdown
 {% else %}
 no shutdown
 {% endif %}
!
{% endfor %}
!
{% if ospf is defined %}
router ospf {{ ospf.process_id }}
 router-id {{ ospf.router_id }}
{% for network in ospf.networks %}
 network {{ network.prefix }} {{ network.wildcard }} area {{ network.area }}
{% endfor %}
{% endif %}
```

```yaml
# playbook using template
- name: Deploy configuration from template
  cisco.ios.ios_config:
    src: templates/router_config.j2
  vars:
    hostname: router1
    interfaces:
      - name: GigabitEthernet0/0
        ip: 10.1.1.1
        mask: 255.255.255.0
        description: WAN Link
    ospf:
      process_id: 1
      router_id: 1.1.1.1
      networks:
        - prefix: 10.1.1.0
          wildcard: 0.0.0.255
          area: 0
```

---

## 5. DNA Center APIs

### DNA Center API Overview

```
DNA Center provides REST APIs for:
• Device inventory
• Site management
• Network health
• Path trace
• Command runner
• Template deployment

Authentication: Token-based (POST /dna/system/api/v1/auth/token)
```

### DNA Center API with Python

```python
import requests
import json

# DNA Center details
dnac = {
    "host": "sandboxdnac.cisco.com",
    "username": "devnetuser",
    "password": "Cisco123!"
}

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Get authentication token
def get_token():
    url = f"https://{dnac['host']}/dna/system/api/v1/auth/token"
    response = requests.post(
        url,
        auth=(dnac["username"], dnac["password"]),
        verify=False
    )
    return response.json()["Token"]

token = get_token()

# Headers with token
headers = {
    "X-Auth-Token": token,
    "Content-Type": "application/json"
}

# Get network devices
def get_devices():
    url = f"https://{dnac['host']}/dna/intent/api/v1/network-device"
    response = requests.get(url, headers=headers, verify=False)
    return response.json()["response"]

devices = get_devices()
for device in devices:
    print(f"{device['hostname']} - {device['managementIpAddress']} - {device['platformId']}")

# Get device health
def get_device_health():
    url = f"https://{dnac['host']}/dna/intent/api/v1/device-health"
    response = requests.get(url, headers=headers, verify=False)
    return response.json()

# Run CLI command on device
def run_command(device_uuid, command):
    url = f"https://{dnac['host']}/dna/intent/api/v1/network-device-poller/cli/read-request"
    payload = {
        "commands": [command],
        "deviceUuids": [device_uuid]
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    task_id = response.json()["response"]["taskId"]
    
    # Poll for result
    task_url = f"https://{dnac['host']}/dna/intent/api/v1/task/{task_id}"
    # ... poll until complete
    return result
```

---

## 6. Embedded Event Manager

### EEM Overview

```
EEM (Embedded Event Manager):
• Automate actions based on events
• Built into IOS
• No external tools needed
• Applets (CLI-based) or TCL scripts

Events: Syslog, SNMP, timers, interface, routing, etc.
Actions: CLI commands, syslog, email, SNMP trap, etc.
```

### EEM Applet Examples

```cisco
! Track interface and send syslog
event manager applet INTERFACE-DOWN
 event syslog pattern "Interface GigabitEthernet0/0, changed state to down"
 action 1.0 syslog msg "ALERT: WAN link down! Switching to backup."
 action 2.0 cli command "enable"
 action 3.0 cli command "configure terminal"
 action 4.0 cli command "ip route 0.0.0.0 0.0.0.0 10.2.2.1"
 action 5.0 cli command "end"

! Scheduled backup
event manager applet NIGHTLY-BACKUP
 event timer cron cron-entry "0 2 * * *"
 action 1.0 cli command "enable"
 action 2.0 cli command "copy running-config tftp://10.1.1.100/$(hostname)-backup.cfg"

! Respond to high CPU
event manager applet HIGH-CPU
 event snmp oid 1.3.6.1.4.1.9.9.109.1.1.1.1.6.1 get-type exact entry-op ge entry-val 80
 action 1.0 syslog msg "CPU HIGH - collecting diagnostics"
 action 2.0 cli command "enable"
 action 3.0 cli command "show processes cpu sorted | redirect flash:cpu-$(timestamp).txt"

! Configuration compliance
event manager applet COMPLIANCE-CHECK
 event syslog pattern "Configured from console"
 action 1.0 syslog msg "Configuration change detected - checking compliance"
 action 2.0 cli command "enable"
 action 3.0 cli command "show run | include no service password-encryption"
 action 4.0 if $_cli_result ne ""
 action 4.1  cli command "configure terminal"
 action 4.2  cli command "service password-encryption"
 action 5.0 end
```

---

## 📝 Module 6 Exercises

### Exercise 6.1: Python Automation
Write a Python script using Netmiko that:
- Connects to multiple devices
- Backs up configurations
- Compares to golden config
- Reports differences

### Exercise 6.2: NETCONF
Use ncclient to:
- Get interface configuration
- Create a new loopback
- Modify interface description

### Exercise 6.3: RESTCONF
Use requests to:
- GET all interfaces via RESTCONF
- PUT a new interface configuration
- PATCH to update description

### Exercise 6.4: EEM
Create an EEM applet that:
- Triggers on login
- Logs username and timestamp
- Sends SNMP trap

---

*Previous: [← Security](../05-security/README.md) | Back to: [README](../../README.md)*

