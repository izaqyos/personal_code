# Module 4: Network Assurance 📊

> **10% of ENCOR Exam | Estimated Time: 20-30 hours**

## Module Overview

Network assurance covers monitoring, analytics, and troubleshooting. Key focus on DNA Center Assurance and modern telemetry.

---

## Table of Contents

1. [Network Management Protocols](#1-network-management-protocols)
2. [DNA Center Assurance](#2-dna-center-assurance)
3. [NetFlow/IPFIX](#3-netflowipfix)
4. [SPAN/RSPAN/ERSPAN](#4-spanrspanerspan)
5. [IP SLA](#5-ip-sla)
6. [Troubleshooting Methodologies](#6-troubleshooting-methodologies)

---

## 1. Network Management Protocols

### SNMP Deep Dive

```
┌─────────────────────────────────────────────────────────────┐
│                    SNMP Architecture                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────┐          ┌────────────┐                    │
│  │   SNMP     │◀────────▶│   SNMP     │                    │
│  │  Manager   │  Get/Set │   Agent    │                    │
│  │  (NMS)     │◀─────────│  (Device)  │                    │
│  └────────────┘   Trap   └────────────┘                    │
│                                                             │
│  Operations:                                                │
│  • GET: Read single OID                                    │
│  • GETNEXT: Read next OID in tree                         │
│  • GETBULK (v2c/v3): Read multiple OIDs                   │
│  • SET: Write to OID                                       │
│  • TRAP: Unsolicited alert from agent                     │
│  • INFORM (v2c/v3): Acknowledged trap                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### SNMPv3 Configuration

```cisco
! Create SNMPv3 group
Router(config)# snmp-server group ADMIN v3 priv

! Create SNMPv3 user
Router(config)# snmp-server user netops ADMIN v3 auth sha AuthP@ss priv aes 256 PrivP@ss

! Configure trap destination
Router(config)# snmp-server host 10.1.1.100 version 3 priv netops

! Enable traps
Router(config)# snmp-server enable traps

! Verification
Router# show snmp user
Router# show snmp group
```

### Streaming Telemetry (Model-Driven)

```
Traditional (SNMP):              Model-Driven Telemetry:
Poll-based, periodic             Push-based, real-time

┌─────┐  Poll  ┌──────┐         ┌─────┐ Stream ┌──────┐
│ NMS │───────▶│Device│         │Coll.│◀───────│Device│
└─────┘        └──────┘         └─────┘        └──────┘
                                
Interval: Minutes               Interval: Seconds
Overhead: High                  Overhead: Low
Data: Limited                   Data: Rich (YANG models)
```

```cisco
! Configure telemetry subscription
Router(config)# telemetry ietf subscription 100
Router(config-mdt-subs)# encoding encode-kvgpb
Router(config-mdt-subs)# filter xpath /interfaces/interface/statistics
Router(config-mdt-subs)# source-address 10.1.1.1
Router(config-mdt-subs)# stream yang-push
Router(config-mdt-subs)# update-policy periodic 1000
Router(config-mdt-subs)# receiver ip address 10.1.1.100 57000 protocol grpc-tcp
```

---

## 2. DNA Center Assurance

### Assurance Features

```
┌─────────────────────────────────────────────────────────────┐
│                  DNA Center Assurance                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Network Health:                                            │
│  ├── Device health scores                                  │
│  ├── Client health (wired/wireless)                        │
│  ├── Application health                                    │
│  └── Trend analysis                                        │
│                                                             │
│  Issue Detection:                                           │
│  ├── AI/ML-driven anomaly detection                        │
│  ├── Proactive issue identification                        │
│  ├── Root cause analysis                                   │
│  └── Guided remediation                                    │
│                                                             │
│  Path Trace:                                                │
│  ├── End-to-end path visualization                         │
│  ├── ACL/QoS policy validation                            │
│  ├── Latency/jitter measurement                           │
│  └── Historical path analysis                              │
│                                                             │
│  Application Experience:                                    │
│  ├── Application response time                             │
│  ├── Network latency vs server latency                     │
│  └── User experience scoring                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Health Scores

```
DNA Center calculates health scores 0-100:

Device Health:
├── Reachability
├── CPU/Memory utilization  
├── Link errors
└── Environmental (temp, power)

Client Health:
├── Onboarding success rate
├── RSSI (wireless)
├── Data rate
└── SNR (signal-to-noise)

Application Health:
├── Response time
├── Packet loss
├── Jitter
└── Throughput
```

---

## 3. NetFlow/IPFIX

### NetFlow Overview

```
NetFlow captures traffic metadata:

┌─────────────────────────────────────────────────────────────┐
│                    NetFlow Record                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Key Fields (define a flow):                               │
│  ├── Source IP                                             │
│  ├── Destination IP                                        │
│  ├── Source Port                                           │
│  ├── Destination Port                                      │
│  ├── Protocol (TCP/UDP/ICMP)                              │
│  ├── Type of Service                                       │
│  └── Input interface                                       │
│                                                             │
│  Non-Key Fields:                                            │
│  ├── Packets count                                         │
│  ├── Bytes count                                           │
│  ├── Start/End timestamps                                  │
│  ├── TCP flags                                             │
│  └── Next-hop                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Flexible NetFlow Configuration

```cisco
! Create flow record
Router(config)# flow record CUSTOM-RECORD
Router(config-flow-record)# match ipv4 source address
Router(config-flow-record)# match ipv4 destination address
Router(config-flow-record)# match transport source-port
Router(config-flow-record)# match transport destination-port
Router(config-flow-record)# match ipv4 protocol
Router(config-flow-record)# collect counter bytes
Router(config-flow-record)# collect counter packets
Router(config-flow-record)# collect timestamp sys-uptime first
Router(config-flow-record)# collect timestamp sys-uptime last

! Create flow exporter
Router(config)# flow exporter EXPORT-TO-COLLECTOR
Router(config-flow-exporter)# destination 10.1.1.100
Router(config-flow-exporter)# transport udp 9996
Router(config-flow-exporter)# source GigabitEthernet0/0

! Create flow monitor
Router(config)# flow monitor TRAFFIC-MONITOR
Router(config-flow-monitor)# record CUSTOM-RECORD
Router(config-flow-monitor)# exporter EXPORT-TO-COLLECTOR
Router(config-flow-monitor)# cache timeout active 60

! Apply to interface
Router(config)# interface GigabitEthernet0/1
Router(config-if)# ip flow monitor TRAFFIC-MONITOR input
Router(config-if)# ip flow monitor TRAFFIC-MONITOR output

! Verification
Router# show flow monitor
Router# show flow record
Router# show flow exporter
```

---

## 4. SPAN/RSPAN/ERSPAN

### SPAN Types Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    SPAN Types                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SPAN (Local):                                              │
│  • Source and destination on same switch                   │
│  • No network overhead                                     │
│                                                             │
│  RSPAN (Remote SPAN):                                       │
│  • Source and destination on different switches            │
│  • Uses RSPAN VLAN to carry mirrored traffic              │
│  • Layer 2 transport                                       │
│                                                             │
│  ERSPAN (Encapsulated RSPAN):                              │
│  • Source and destination anywhere (routed)               │
│  • GRE encapsulation                                       │
│  • Layer 3 transport                                       │
│                                                             │
│  ┌───────┐                     ┌───────┐                   │
│  │ SPAN  │ Same switch         │Analyzer│                  │
│  │Source │────────────────────▶│        │                  │
│  └───────┘                     └───────┘                   │
│                                                             │
│  ┌───────┐     RSPAN VLAN     ┌───────┐                   │
│  │ RSPAN │════════════════════│Analyzer│                  │
│  │Source │ (L2 trunk)         │        │                  │
│  └───────┘                     └───────┘                   │
│                                                             │
│  ┌───────┐     GRE Tunnel     ┌───────┐                   │
│  │ERSPAN │~~~~~~~~~~~~~~~~~~~~│Analyzer│                  │
│  │Source │ (L3 routed)        │        │                  │
│  └───────┘                     └───────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### SPAN Configuration

```cisco
! Local SPAN
Switch(config)# monitor session 1 source interface gi0/1 both
Switch(config)# monitor session 1 destination interface gi0/24

! RSPAN (Source Switch)
Switch(config)# vlan 999
Switch(config-vlan)# remote-span
Switch(config)# monitor session 1 source interface gi0/1
Switch(config)# monitor session 1 destination remote vlan 999

! RSPAN (Destination Switch)
Switch(config)# vlan 999
Switch(config-vlan)# remote-span
Switch(config)# monitor session 1 source remote vlan 999
Switch(config)# monitor session 1 destination interface gi0/24

! ERSPAN (Source)
Switch(config)# monitor session 1 type erspan-source
Switch(config-mon-erspan-src)# source interface gi0/1
Switch(config-mon-erspan-src)# destination
Switch(config-mon-erspan-src-dst)# erspan-id 100
Switch(config-mon-erspan-src-dst)# ip address 10.1.1.100
Switch(config-mon-erspan-src-dst)# origin ip address 10.1.1.1

! Verification
Switch# show monitor session 1
```

---

## 5. IP SLA

### IP SLA Overview

```
IP SLA (Service Level Agreement):
• Active network monitoring
• Simulates traffic and measures performance
• Can trigger actions based on results

Common Probes:
├── ICMP Echo (ping)
├── UDP Jitter
├── HTTP (web response)
├── DNS
├── TCP Connect
└── VoIP (jitter, MOS score)
```

### IP SLA Configuration

```cisco
! ICMP Echo probe
Router(config)# ip sla 1
Router(config-ip-sla)# icmp-echo 10.1.1.100 source-ip 10.1.1.1
Router(config-ip-sla-echo)# frequency 30
Router(config-ip-sla-echo)# threshold 100

! UDP Jitter probe (VoIP simulation)
Router(config)# ip sla 2
Router(config-ip-sla)# udp-jitter 10.1.1.100 16384 codec g711alaw
Router(config-ip-sla-jitter)# frequency 60

! Schedule the probe
Router(config)# ip sla schedule 1 start-time now life forever
Router(config)# ip sla schedule 2 start-time now life forever

! Track for failover
Router(config)# track 1 ip sla 1 reachability
Router(config)# ip route 0.0.0.0 0.0.0.0 10.1.1.1 track 1
Router(config)# ip route 0.0.0.0 0.0.0.0 10.2.2.1 10  ! Backup

! Verification
Router# show ip sla statistics
Router# show ip sla configuration
Router# show track 1
```

---

## 6. Troubleshooting Methodologies

### Structured Approach

```
┌─────────────────────────────────────────────────────────────┐
│              OSI-Based Troubleshooting                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Bottom-Up:                   Top-Down:                    │
│  Start at Physical           Start at Application          │
│  ↓                            ↑                            │
│  L1 Physical                  L7 Application               │
│  L2 Data Link                 L6 Presentation              │
│  L3 Network                   L5 Session                   │
│  L4 Transport                 L4 Transport                 │
│  L5 Session                   L3 Network                   │
│  L6 Presentation              L2 Data Link                 │
│  L7 Application               L1 Physical                  │
│                                                             │
│  Divide-and-Conquer:                                       │
│  Start at L3, expand up or down based on results          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Troubleshooting Commands

```cisco
! Layer 1-2
show interfaces
show interfaces status
show interfaces counters errors
show mac address-table

! Layer 2 Specific
show spanning-tree
show etherchannel summary
show vlan brief

! Layer 3
show ip interface brief
show ip route
show ip arp
show ip protocols

! Routing Protocol Specific
show ip ospf neighbor
show ip ospf database
show ip eigrp neighbors
show ip eigrp topology
show bgp summary
show bgp ipv4 unicast

! Path Testing
ping [destination] source [source]
traceroute [destination]
show ip cef [destination]

! Debug (use carefully!)
debug ip packet
debug ip routing
debug ip ospf adj
undebug all
```

---

## 📝 Module 4 Exercises

### Exercise 4.1: NetFlow
Configure Flexible NetFlow to:
- Capture source/dest IP, ports, protocol
- Export to collector at 10.1.1.100:9996
- 60-second active timeout

### Exercise 4.2: IP SLA
Configure IP SLA for:
- Primary path via 10.1.1.1
- Backup path via 10.2.2.1
- Failover when latency exceeds 100ms

### Exercise 4.3: ERSPAN
Configure ERSPAN to mirror traffic from a remote switch to an analyzer.

---

*Previous: [← Infrastructure](../03-infrastructure/README.md) | Next: [Security →](../05-security/README.md)*

