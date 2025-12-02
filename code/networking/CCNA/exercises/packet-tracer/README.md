# Packet Tracer Labs 🖥️

> **Hands-on labs using Cisco Packet Tracer**

## Getting Started

1. Download [Cisco Packet Tracer](https://www.netacad.com/courses/packet-tracer) (free with NetAcad account)
2. Open each `.pkt` file (or build from instructions below)
3. Complete the objectives
4. Verify with provided test cases

---

## Lab Index

| Lab | Module | Difficulty | Time |
|-----|--------|------------|------|
| [Lab 1](#lab-1-basic-switch-configuration) | M1 | ⭐ | 30 min |
| [Lab 2](#lab-2-vlan-configuration) | M2 | ⭐⭐ | 45 min |
| [Lab 3](#lab-3-inter-vlan-routing) | M2 | ⭐⭐ | 45 min |
| [Lab 4](#lab-4-stp-configuration) | M2 | ⭐⭐⭐ | 60 min |
| [Lab 5](#lab-5-static-routing) | M3 | ⭐⭐ | 45 min |
| [Lab 6](#lab-6-ospf-single-area) | M3 | ⭐⭐⭐ | 60 min |
| [Lab 7](#lab-7-ospf-multi-area) | M3 | ⭐⭐⭐ | 75 min |
| [Lab 8](#lab-8-nat-configuration) | M4 | ⭐⭐ | 45 min |
| [Lab 9](#lab-9-dhcp-server) | M4 | ⭐⭐ | 30 min |
| [Lab 10](#lab-10-acl-implementation) | M5 | ⭐⭐⭐ | 60 min |

---

## Lab 1: Basic Switch Configuration

### Topology
```
        ┌─────────┐
        │   SW1   │
        └────┬────┘
             │
    ┌────────┼────────┐
    │        │        │
  ┌─┴─┐    ┌─┴─┐    ┌─┴─┐
  │PC1│    │PC2│    │PC3│
  └───┘    └───┘    └───┘
```

### Objectives
1. Configure hostname
2. Set enable secret password
3. Configure console and VTY passwords
4. Configure management VLAN
5. Configure banner MOTD
6. Save configuration

### Instructions

```cisco
! 1. Set hostname
Switch> enable
Switch# configure terminal
Switch(config)# hostname SW1

! 2. Set enable secret
SW1(config)# enable secret cisco123

! 3. Configure console password
SW1(config)# line console 0
SW1(config-line)# password console123
SW1(config-line)# login
SW1(config-line)# exit

! 4. Configure VTY password
SW1(config)# line vty 0 4
SW1(config-line)# password vty123
SW1(config-line)# login
SW1(config-line)# exit

! 5. Configure management VLAN and IP
SW1(config)# interface vlan 1
SW1(config-if)# ip address 192.168.1.2 255.255.255.0
SW1(config-if)# no shutdown
SW1(config-if)# exit
SW1(config)# ip default-gateway 192.168.1.1

! 6. Configure banner
SW1(config)# banner motd # Authorized Access Only #

! 7. Save configuration
SW1(config)# end
SW1# copy running-config startup-config
```

### Verification
```cisco
SW1# show running-config
SW1# show interface vlan 1
SW1# show ip interface brief
```

---

## Lab 2: VLAN Configuration

### Topology
```
                    ┌─────────┐
                    │   SW1   │
                    └────┬────┘
           Trunk         │
                    ┌────┴────┐
                    │   SW2   │
                    └────┬────┘
                         │
    ┌──────────┬─────────┼──────────┬──────────┐
    │          │         │          │          │
  ┌─┴─┐      ┌─┴─┐     ┌─┴─┐      ┌─┴─┐      ┌─┴─┐
  │PC1│      │PC2│     │PC3│      │PC4│      │PC5│
  └───┘      └───┘     └───┘      └───┘      └───┘
 VLAN10     VLAN10    VLAN20     VLAN20     VLAN30
```

### Objectives
1. Create VLANs 10, 20, 30
2. Assign ports to VLANs
3. Configure trunk between switches
4. Verify VLAN operation

### IP Addressing
| Device | VLAN | IP Address |
|--------|------|------------|
| PC1 | 10 | 192.168.10.1/24 |
| PC2 | 10 | 192.168.10.2/24 |
| PC3 | 20 | 192.168.20.1/24 |
| PC4 | 20 | 192.168.20.2/24 |
| PC5 | 30 | 192.168.30.1/24 |

### Instructions

```cisco
! On SW2
SW2(config)# vlan 10
SW2(config-vlan)# name SALES
SW2(config-vlan)# vlan 20
SW2(config-vlan)# name ENGINEERING
SW2(config-vlan)# vlan 30
SW2(config-vlan)# name MANAGEMENT
SW2(config-vlan)# exit

! Assign access ports
SW2(config)# interface range fa0/1-2
SW2(config-if-range)# switchport mode access
SW2(config-if-range)# switchport access vlan 10

SW2(config)# interface range fa0/3-4
SW2(config-if-range)# switchport mode access
SW2(config-if-range)# switchport access vlan 20

SW2(config)# interface fa0/5
SW2(config-if)# switchport mode access
SW2(config-if)# switchport access vlan 30

! Configure trunk to SW1
SW2(config)# interface gi0/1
SW2(config-if)# switchport mode trunk
SW2(config-if)# switchport trunk allowed vlan 10,20,30
```

### Verification
```cisco
SW2# show vlan brief
SW2# show interfaces trunk
SW2# show interfaces fa0/1 switchport
```

### Test Cases
- [ ] PC1 can ping PC2 (same VLAN)
- [ ] PC3 can ping PC4 (same VLAN)
- [ ] PC1 cannot ping PC3 (different VLANs)

---

## Lab 3: Inter-VLAN Routing

### Topology
```
                    ┌─────────┐
                    │   R1    │
                    │ (RoaS)  │
                    └────┬────┘
                         │ Trunk (Gi0/0)
                    ┌────┴────┐
                    │   SW1   │
                    └────┬────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
  ┌─┴─┐                ┌─┴─┐                ┌─┴─┐
  │PC1│                │PC2│                │PC3│
  └───┘                └───┘                └───┘
 VLAN10               VLAN20               VLAN30
```

### Objectives
1. Configure Router-on-a-Stick
2. Create subinterfaces for each VLAN
3. Enable inter-VLAN routing
4. Test connectivity between VLANs

### IP Addressing
| Interface | VLAN | IP Address | Gateway |
|-----------|------|------------|---------|
| R1 Gi0/0.10 | 10 | 192.168.10.1/24 | - |
| R1 Gi0/0.20 | 20 | 192.168.20.1/24 | - |
| R1 Gi0/0.30 | 30 | 192.168.30.1/24 | - |
| PC1 | 10 | 192.168.10.10/24 | .1 |
| PC2 | 20 | 192.168.20.10/24 | .1 |
| PC3 | 30 | 192.168.30.10/24 | .1 |

### Instructions

```cisco
! On R1
R1(config)# interface gi0/0
R1(config-if)# no shutdown

R1(config)# interface gi0/0.10
R1(config-subif)# encapsulation dot1q 10
R1(config-subif)# ip address 192.168.10.1 255.255.255.0

R1(config)# interface gi0/0.20
R1(config-subif)# encapsulation dot1q 20
R1(config-subif)# ip address 192.168.20.1 255.255.255.0

R1(config)# interface gi0/0.30
R1(config-subif)# encapsulation dot1q 30
R1(config-subif)# ip address 192.168.30.1 255.255.255.0
```

### Verification
```cisco
R1# show ip interface brief
R1# show interfaces gi0/0.10
R1# show ip route
```

### Test Cases
- [ ] PC1 can ping R1 Gi0/0.10 (192.168.10.1)
- [ ] PC1 can ping PC2 (192.168.20.10)
- [ ] PC1 can ping PC3 (192.168.30.10)
- [ ] All PCs can ping all gateways

---

## Lab 4: STP Configuration

### Topology
```
        ┌─────────┐
        │   SW1   │──────────┐
        │  (Root) │          │
        └────┬────┘          │
             │               │
        ┌────┴────┐     ┌────┴────┐
        │   SW2   │─────│   SW3   │
        └─────────┘     └─────────┘
```

### Objectives
1. Verify default STP election
2. Configure SW1 as root bridge
3. Identify port roles (Root, Designated, Blocked)
4. Configure PortFast and BPDU Guard

### Instructions

```cisco
! Check current STP status
SW1# show spanning-tree

! Make SW1 root bridge for VLAN 1
SW1(config)# spanning-tree vlan 1 root primary
! Or manually
SW1(config)# spanning-tree vlan 1 priority 4096

! Enable Rapid PVST+
SW1(config)# spanning-tree mode rapid-pvst

! Configure PortFast on access ports
SW2(config)# interface range fa0/1-10
SW2(config-if-range)# spanning-tree portfast
SW2(config-if-range)# spanning-tree bpduguard enable
```

### Verification
```cisco
SW1# show spanning-tree
SW1# show spanning-tree root
SW1# show spanning-tree interface fa0/1
```

---

## Lab 5: Static Routing

### Topology
```
┌────────┐       ┌────────┐       ┌────────┐
│   R1   │───────│   R2   │───────│   R3   │
└───┬────┘       └────────┘       └────┬───┘
    │                                  │
 10.1.1.0/24                      10.3.3.0/24
    │                                  │
  ┌─┴─┐                              ┌─┴─┐
  │PC1│                              │PC2│
  └───┘                              └───┘
```

### IP Addressing
| Interface | IP Address |
|-----------|------------|
| R1 Gi0/0 | 10.1.1.1/24 |
| R1 Gi0/1 | 10.12.12.1/30 |
| R2 Gi0/0 | 10.12.12.2/30 |
| R2 Gi0/1 | 10.23.23.1/30 |
| R3 Gi0/0 | 10.23.23.2/30 |
| R3 Gi0/1 | 10.3.3.1/24 |
| PC1 | 10.1.1.10/24 (GW: .1) |
| PC2 | 10.3.3.10/24 (GW: .1) |

### Instructions

```cisco
! R1 - Route to PC2 network via R2
R1(config)# ip route 10.3.3.0 255.255.255.0 10.12.12.2
R1(config)# ip route 10.23.23.0 255.255.255.252 10.12.12.2

! R2 - Routes to both end networks
R2(config)# ip route 10.1.1.0 255.255.255.0 10.12.12.1
R2(config)# ip route 10.3.3.0 255.255.255.0 10.23.23.2

! R3 - Route to PC1 network via R2
R3(config)# ip route 10.1.1.0 255.255.255.0 10.23.23.1
R3(config)# ip route 10.12.12.0 255.255.255.252 10.23.23.1
```

### Verification
```cisco
R1# show ip route
R1# traceroute 10.3.3.10
```

### Test Cases
- [ ] PC1 can ping R2 (10.12.12.2)
- [ ] PC1 can ping R3 (10.3.3.1)
- [ ] PC1 can ping PC2 (10.3.3.10)

---

## Lab 6: OSPF Single-Area

### Topology
```
                    Area 0
┌────────┐       ┌────────┐       ┌────────┐
│   R1   │───────│   R2   │───────│   R3   │
└───┬────┘       └────────┘       └────┬───┘
    │                                  │
 LAN1                                LAN3
```

### Objectives
1. Configure OSPF on all routers
2. Set router IDs
3. Verify neighbor adjacency
4. Verify routing table

### Instructions

```cisco
! R1 Configuration
R1(config)# router ospf 1
R1(config-router)# router-id 1.1.1.1
R1(config-router)# network 10.1.1.0 0.0.0.255 area 0
R1(config-router)# network 10.12.12.0 0.0.0.3 area 0
R1(config-router)# passive-interface gi0/0

! R2 Configuration
R2(config)# router ospf 1
R2(config-router)# router-id 2.2.2.2
R2(config-router)# network 10.12.12.0 0.0.0.3 area 0
R2(config-router)# network 10.23.23.0 0.0.0.3 area 0

! R3 Configuration
R3(config)# router ospf 1
R3(config-router)# router-id 3.3.3.3
R3(config-router)# network 10.23.23.0 0.0.0.3 area 0
R3(config-router)# network 10.3.3.0 0.0.0.255 area 0
R3(config-router)# passive-interface gi0/1
```

### Verification
```cisco
R1# show ip ospf neighbor
R1# show ip ospf interface brief
R1# show ip route ospf
R1# show ip ospf database
```

---

## More Labs Available

Labs 7-10 follow similar patterns for:
- **Lab 7**: OSPF Multi-Area (ABR configuration)
- **Lab 8**: NAT/PAT Configuration
- **Lab 9**: DHCP Server Setup
- **Lab 10**: ACL Implementation

Build these topologies in Packet Tracer and practice!

---

## Lab Tips

1. **Save frequently** - Use `copy run start`
2. **Document everything** - Use `description` on interfaces
3. **Test incrementally** - Verify each step before moving on
4. **Use debug carefully** - `debug ip ospf adj` can help troubleshooting
5. **Check connectivity first** - Layer 1/2 before Layer 3

---

*Back to: [Exercises](../README.md)*

