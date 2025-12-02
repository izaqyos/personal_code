# Troubleshooting Scenarios 🔍

> **Real-world troubleshooting scenarios to test your skills**

## Troubleshooting Methodology

```
┌─────────────────────────────────────────────────────────────┐
│                Systematic Approach                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Define the Problem                                      │
│     • What is happening vs. what should happen?            │
│     • When did it start?                                   │
│     • What changed?                                        │
│                                                             │
│  2. Gather Information                                      │
│     • show commands                                        │
│     • Logs                                                 │
│     • User reports                                         │
│                                                             │
│  3. Analyze Information                                     │
│     • Compare to baseline                                  │
│     • Identify patterns                                    │
│     • Layer-by-layer analysis                              │
│                                                             │
│  4. Propose Hypothesis                                      │
│     • Educated guess based on evidence                     │
│                                                             │
│  5. Test Hypothesis                                         │
│     • Make minimal changes                                 │
│     • Verify results                                       │
│                                                             │
│  6. Solve or Escalate                                       │
│     • Document solution                                    │
│     • Or escalate with findings                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Scenario 1: VLAN Connectivity Issue

### Problem Statement
PC1 in VLAN 10 cannot ping PC2 in VLAN 10 on a different switch.

### Topology
```
        ┌─────────┐              ┌─────────┐
PC1 ────│   SW1   │──────────────│   SW2   │──── PC2
VLAN 10 └─────────┘    Trunk?    └─────────┘ VLAN 10
```

### Troubleshooting Steps

```cisco
! Step 1: Verify PC1 VLAN assignment
SW1# show vlan brief
SW1# show interfaces fa0/1 switchport

! Step 2: Verify trunk status
SW1# show interfaces trunk
SW1# show interfaces gi0/1 switchport

! Step 3: Check allowed VLANs on trunk
SW1# show interfaces trunk | include allowed

! Step 4: Verify VLAN exists on both switches
SW2# show vlan brief
```

### Common Causes
- [ ] Port not in correct VLAN
- [ ] Trunk not formed (DTP issues)
- [ ] VLAN not allowed on trunk
- [ ] VLAN doesn't exist on remote switch
- [ ] Native VLAN mismatch

### Solution Checklist
```cisco
! Fix: Port not in VLAN
SW1(config)# interface fa0/1
SW1(config-if)# switchport access vlan 10

! Fix: Trunk not formed
SW1(config)# interface gi0/1
SW1(config-if)# switchport mode trunk

! Fix: VLAN not allowed
SW1(config-if)# switchport trunk allowed vlan add 10

! Fix: VLAN doesn't exist
SW2(config)# vlan 10
SW2(config-vlan)# name SALES
```

---

## Scenario 2: OSPF Neighbor Not Forming

### Problem Statement
R1 and R2 are not forming an OSPF adjacency.

### Topology
```
┌────────┐               ┌────────┐
│   R1   │───────────────│   R2   │
│ OSPF 1 │  10.1.1.0/30  │ OSPF 1 │
└────────┘               └────────┘
```

### Troubleshooting Steps

```cisco
! Step 1: Verify Layer 1/2 connectivity
R1# ping 10.1.1.2

! Step 2: Check OSPF neighbor status
R1# show ip ospf neighbor

! Step 3: Verify OSPF interface configuration
R1# show ip ospf interface gi0/0
R2# show ip ospf interface gi0/0

! Step 4: Compare critical parameters
R1# show ip ospf interface gi0/0 | include Hello|Dead|Area|Network Type

! Step 5: Check for ACLs blocking OSPF
R1# show access-lists
R1# show ip interface gi0/0
```

### OSPF Neighbor Requirements Checklist
- [ ] Same area ID
- [ ] Same subnet
- [ ] Same Hello/Dead timers
- [ ] Same authentication
- [ ] Same network type
- [ ] MTU match (for Full state)
- [ ] Router ID unique

### Solution Checklist
```cisco
! Fix: Hello/Dead timer mismatch
R1(config-if)# ip ospf hello-interval 10
R1(config-if)# ip ospf dead-interval 40

! Fix: Area mismatch
R1(config-router)# network 10.1.1.0 0.0.0.3 area 0

! Fix: Authentication mismatch
R1(config-if)# ip ospf authentication message-digest
R1(config-if)# ip ospf message-digest-key 1 md5 MyKey

! Fix: Network type mismatch
R1(config-if)# ip ospf network point-to-point

! Fix: MTU mismatch (temporary)
R1(config-if)# ip ospf mtu-ignore
```

---

## Scenario 3: NAT Not Working

### Problem Statement
Internal users (192.168.1.0/24) cannot access the internet.

### Topology
```
┌───────────────┐         ┌────────┐
│ 192.168.1.0/24│─────────│ Router │─────────── Internet
│   Internal    │  gi0/0  │  NAT   │  gi0/1
└───────────────┘         └────────┘
```

### Troubleshooting Steps

```cisco
! Step 1: Verify NAT translations
R1# show ip nat translations
R1# show ip nat statistics

! Step 2: Check inside/outside interface marking
R1# show ip interface gi0/0 | include NAT
R1# show ip interface gi0/1 | include NAT

! Step 3: Verify ACL for NAT
R1# show access-lists

! Step 4: Check routing
R1# show ip route
R1# ping 8.8.8.8
```

### Common Causes
- [ ] Inside/outside not configured
- [ ] ACL doesn't match source traffic
- [ ] No route to destination
- [ ] NAT pool exhausted

### Solution Checklist
```cisco
! Fix: Missing inside/outside
R1(config)# interface gi0/0
R1(config-if)# ip nat inside
R1(config)# interface gi0/1
R1(config-if)# ip nat outside

! Fix: ACL not matching
R1(config)# access-list 1 permit 192.168.1.0 0.0.0.255

! Fix: NAT not configured
R1(config)# ip nat inside source list 1 interface gi0/1 overload
```

---

## Scenario 4: STP Blocking Wrong Port

### Problem Statement
Traffic taking a suboptimal path due to incorrect root bridge election.

### Topology
```
        ┌─────────┐
        │  SW1    │ (Should be root)
        │ 10 Gbps │
        └────┬────┘
             │
    ┌────────┴────────┐
    │                 │
┌───┴───┐         ┌───┴───┐
│  SW2  │─────────│  SW3  │ (Is root!)
│ 1 Gbps│         │ 1 Gbps│
└───────┘         └───────┘
```

### Troubleshooting Steps

```cisco
! Step 1: Find current root bridge
SW1# show spanning-tree root

! Step 2: Check bridge priorities
SW1# show spanning-tree | include Bridge ID
SW2# show spanning-tree | include Bridge ID
SW3# show spanning-tree | include Bridge ID

! Step 3: Identify port roles and states
SW1# show spanning-tree interface gi0/1

! Step 4: Check spanning-tree mode
SW1# show spanning-tree summary
```

### Solution Checklist
```cisco
! Make SW1 root bridge
SW1(config)# spanning-tree vlan 1 root primary
! OR
SW1(config)# spanning-tree vlan 1 priority 4096

! Make SW2 secondary root
SW2(config)# spanning-tree vlan 1 root secondary
```

---

## Scenario 5: DHCP Not Working

### Problem Statement
Clients not receiving IP addresses from DHCP server.

### Topology
```
┌────────┐                ┌────────┐         ┌────────────┐
│ Client │────────────────│ Router │─────────│ DHCP Server│
│        │     VLAN 10    │(Relay) │         │ 10.1.1.100 │
└────────┘                └────────┘         └────────────┘
```

### Troubleshooting Steps

```cisco
! Step 1: Check if DHCP server is reachable
R1# ping 10.1.1.100

! Step 2: Verify DHCP pool (if router is server)
R1# show ip dhcp pool
R1# show ip dhcp binding
R1# show ip dhcp server statistics

! Step 3: Check helper address (if using relay)
R1# show running-config interface gi0/0 | include helper

! Step 4: Check for DHCP snooping issues
SW1# show ip dhcp snooping
SW1# show ip dhcp snooping binding

! Step 5: Verify excluded addresses
R1# show running-config | include excluded
```

### Common Causes
- [ ] DHCP server unreachable
- [ ] No helper address (relay)
- [ ] Pool exhausted
- [ ] DHCP snooping blocking legitimate server
- [ ] Wrong excluded addresses

### Solution Checklist
```cisco
! Fix: Add helper address
R1(config)# interface gi0/0
R1(config-if)# ip helper-address 10.1.1.100

! Fix: Trust DHCP snooping port
SW1(config)# interface gi0/1
SW1(config-if)# ip dhcp snooping trust

! Fix: Pool exhausted - check bindings
R1# clear ip dhcp binding *
```

---

## Scenario 6: ACL Blocking Legitimate Traffic

### Problem Statement
Users cannot access web server after ACL was applied.

### Troubleshooting Steps

```cisco
! Step 1: View ACL with hit counts
R1# show access-lists

! Step 2: Check where ACL is applied
R1# show ip interface gi0/0 | include access list

! Step 3: Test with specific traffic
R1# debug ip packet detail

! Step 4: Verify ACL order
R1# show access-list MYACL
```

### ACL Troubleshooting Tips
- Remember implicit deny at end
- ACEs processed top to bottom
- First match wins
- Check direction (in/out)
- Use `log` keyword for visibility

### Solution Checklist
```cisco
! Fix: Add missing permit before deny
R1(config)# ip access-list extended MYACL
R1(config-ext-nacl)# 15 permit tcp any any eq 443
! (Insert before deny statement)

! Fix: Remove overly broad deny
R1(config-ext-nacl)# no deny ip any any
```

---

## Quick Diagnostic Commands

| Issue | Command |
|-------|---------|
| Layer 1 | `show interfaces status` |
| Layer 2 | `show mac address-table` |
| VLANs | `show vlan brief` |
| Trunks | `show interfaces trunk` |
| STP | `show spanning-tree` |
| Routes | `show ip route` |
| OSPF | `show ip ospf neighbor` |
| NAT | `show ip nat translations` |
| ACLs | `show access-lists` |
| DHCP | `show ip dhcp binding` |

---

*Back to: [Exercises](../README.md)*

