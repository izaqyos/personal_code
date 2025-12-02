# CLI Drills 💻

> **Practice essential commands until they become muscle memory**

## How to Use

1. Cover the "Answer" column
2. Type the command from memory
3. Check your answer
4. Repeat until perfect

---

## Basic Device Configuration

| Task | Answer |
|------|--------|
| Enter privileged mode | `enable` |
| Enter global config | `configure terminal` |
| Set hostname to "R1" | `hostname R1` |
| Set enable secret | `enable secret MyPassword` |
| Encrypt all passwords | `service password-encryption` |
| Set banner MOTD | `banner motd # Message #` |
| Save configuration | `copy running-config startup-config` |
| View running config | `show running-config` |
| View startup config | `show startup-config` |
| Erase startup config | `erase startup-config` |

---

## Interface Configuration

| Task | Answer |
|------|--------|
| Enter interface config | `interface gi0/0` |
| Set IP address | `ip address 192.168.1.1 255.255.255.0` |
| Enable interface | `no shutdown` |
| Disable interface | `shutdown` |
| Set interface description | `description WAN Link to ISP` |
| View all interfaces | `show ip interface brief` |
| View specific interface | `show interface gi0/0` |
| View interface status | `show interfaces status` |

---

## VLAN Configuration

| Task | Answer |
|------|--------|
| Create VLAN 10 | `vlan 10` |
| Name VLAN | `name SALES` |
| Set port to access mode | `switchport mode access` |
| Assign port to VLAN 10 | `switchport access vlan 10` |
| Set port to trunk mode | `switchport mode trunk` |
| Set native VLAN on trunk | `switchport trunk native vlan 99` |
| Allow specific VLANs on trunk | `switchport trunk allowed vlan 10,20,30` |
| View VLANs | `show vlan brief` |
| View trunk status | `show interfaces trunk` |

---

## Routing - Static

| Task | Answer |
|------|--------|
| Static route to network | `ip route 192.168.2.0 255.255.255.0 10.1.1.2` |
| Default route | `ip route 0.0.0.0 0.0.0.0 10.1.1.1` |
| Floating static (AD 100) | `ip route 192.168.2.0 255.255.255.0 10.2.2.2 100` |
| View routing table | `show ip route` |
| View static routes only | `show ip route static` |

---

## Routing - OSPF

| Task | Answer |
|------|--------|
| Enable OSPF process | `router ospf 1` |
| Set router ID | `router-id 1.1.1.1` |
| Advertise network | `network 192.168.1.0 0.0.0.255 area 0` |
| Enable on interface | `ip ospf 1 area 0` (interface config) |
| Make passive interface | `passive-interface gi0/0` |
| Set reference bandwidth | `auto-cost reference-bandwidth 10000` |
| View OSPF neighbors | `show ip ospf neighbor` |
| View OSPF interfaces | `show ip ospf interface brief` |
| View OSPF database | `show ip ospf database` |
| View OSPF routes | `show ip route ospf` |

---

## NAT Configuration

| Task | Answer |
|------|--------|
| Mark inside interface | `ip nat inside` |
| Mark outside interface | `ip nat outside` |
| Static NAT | `ip nat inside source static 192.168.1.10 203.0.113.10` |
| NAT pool | `ip nat pool MYPOOL 203.0.113.1 203.0.113.5 netmask 255.255.255.0` |
| PAT with interface | `ip nat inside source list 1 interface gi0/1 overload` |
| PAT with pool | `ip nat inside source list 1 pool MYPOOL overload` |
| View NAT translations | `show ip nat translations` |
| View NAT statistics | `show ip nat statistics` |
| Clear NAT translations | `clear ip nat translation *` |

---

## DHCP Configuration

| Task | Answer |
|------|--------|
| Create DHCP pool | `ip dhcp pool LAN_POOL` |
| Set network | `network 192.168.1.0 255.255.255.0` |
| Set default gateway | `default-router 192.168.1.1` |
| Set DNS server | `dns-server 8.8.8.8` |
| Exclude addresses | `ip dhcp excluded-address 192.168.1.1 192.168.1.10` |
| View DHCP bindings | `show ip dhcp binding` |
| View DHCP pool | `show ip dhcp pool` |
| Configure relay agent | `ip helper-address 10.1.1.100` |

---

## ACL Configuration

| Task | Answer |
|------|--------|
| Standard ACL (numbered) | `access-list 10 permit 192.168.1.0 0.0.0.255` |
| Standard ACL (named) | `ip access-list standard MYACL` |
| Extended ACL (named) | `ip access-list extended MYACL` |
| Permit HTTP | `permit tcp any any eq 80` |
| Permit HTTPS | `permit tcp any any eq 443` |
| Deny with log | `deny ip any any log` |
| Apply ACL inbound | `ip access-group MYACL in` |
| Apply ACL outbound | `ip access-group MYACL out` |
| View ACLs | `show access-lists` |
| View specific ACL | `show access-lists MYACL` |

---

## Security Configuration

| Task | Answer |
|------|--------|
| Enable port security | `switchport port-security` |
| Set max MAC addresses | `switchport port-security maximum 2` |
| Sticky MAC learning | `switchport port-security mac-address sticky` |
| Violation shutdown | `switchport port-security violation shutdown` |
| Enable DHCP snooping | `ip dhcp snooping` |
| DHCP snooping on VLAN | `ip dhcp snooping vlan 10` |
| Trust DHCP snooping port | `ip dhcp snooping trust` |
| Enable DAI | `ip arp inspection vlan 10` |
| View port security | `show port-security interface fa0/1` |

---

## SSH Configuration

| Task | Answer |
|------|--------|
| Set domain name | `ip domain-name example.com` |
| Generate RSA keys | `crypto key generate rsa modulus 2048` |
| Set SSH version 2 | `ip ssh version 2` |
| Create local user | `username admin privilege 15 secret MyPass` |
| VTY SSH only | `transport input ssh` |
| VTY local login | `login local` |
| View SSH status | `show ip ssh` |
| View SSH sessions | `show ssh` |

---

## NTP & Syslog

| Task | Answer |
|------|--------|
| Configure NTP server | `ntp server 216.239.35.0` |
| Set as NTP master | `ntp master 4` |
| View NTP status | `show ntp status` |
| View NTP associations | `show ntp associations` |
| Set syslog server | `logging host 10.1.1.100` |
| Set syslog level | `logging trap informational` |
| View logs | `show logging` |

---

## Troubleshooting Commands

| Task | Answer |
|------|--------|
| Ping | `ping 192.168.1.1` |
| Extended ping | `ping` (then follow prompts) |
| Traceroute | `traceroute 192.168.1.1` |
| View ARP table | `show arp` |
| View MAC table | `show mac address-table` |
| View CDP neighbors | `show cdp neighbors` |
| View CDP detail | `show cdp neighbors detail` |
| Debug OSPF adjacency | `debug ip ospf adj` |
| Turn off debugging | `undebug all` |

---

## Speed Drill Challenge

**Goal**: Complete all commands in under 5 minutes

1. Set hostname to "R1"
2. Set enable secret to "cisco"
3. Create user "admin" with password "admin123"
4. Configure Gi0/0 with IP 192.168.1.1/24
5. Enable the interface
6. Create OSPF process 1 with router-id 1.1.1.1
7. Advertise 192.168.1.0/24 in area 0
8. Enable SSH version 2
9. Generate 2048-bit RSA keys
10. Configure VTY for SSH only with local login
11. Save configuration

**Time yourself and track improvement!**

---

*Back to: [Exercises](../README.md)*

