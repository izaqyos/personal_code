# CCNP Quick Reference 📋

## Routing Protocol Comparison

| Protocol | AD | Metric | Algorithm | Type |
|----------|-----|--------|-----------|------|
| Connected | 0 | - | - | - |
| Static | 1 | - | - | - |
| EIGRP | 90 | Composite (BW+Delay) | DUAL | Hybrid |
| OSPF | 110 | Cost (BW) | Dijkstra | Link-State |
| eBGP | 20 | Path Attributes | Best Path | Path Vector |
| iBGP | 200 | Path Attributes | Best Path | Path Vector |

---

## BGP Path Selection

1. **Weight** (highest) - Cisco, local
2. **Local Preference** (highest) - iBGP
3. **Locally originated** - local routes
4. **AS-Path** (shortest)
5. **Origin** (IGP < EGP < ?)
6. **MED** (lowest) - between ASes
7. **eBGP over iBGP**
8. **IGP metric** to next-hop (lowest)
9. **Oldest route**
10. **Router ID** (lowest)

---

## OSPF LSA Types

| Type | Name | Scope | Generator |
|------|------|-------|-----------|
| 1 | Router | Area | All routers |
| 2 | Network | Area | DR |
| 3 | Summary | Domain | ABR |
| 4 | ASBR Summary | Domain | ABR |
| 5 | External | Domain | ASBR |
| 7 | NSSA External | NSSA | ASBR in NSSA |

---

## OSPF Area Types

| Type | LSA 3 | LSA 5 | LSA 7 | Default |
|------|-------|-------|-------|---------|
| Standard | ✓ | ✓ | - | - |
| Stub | ✓ | ✗ | - | ABR injects |
| Totally Stubby | ✗ | ✗ | - | ABR injects |
| NSSA | ✓ | ✗ | ✓ | Optional |
| Totally NSSA | ✗ | ✗ | ✓ | ABR injects |

---

## EIGRP Terminology

| Term | Description |
|------|-------------|
| FD | Feasible Distance - total metric |
| RD | Reported Distance - neighbor's metric |
| Successor | Best route |
| Feasible Successor | Backup (RD < current FD) |
| K-values | K1=BW, K2=Load, K3=Delay, K4=Reliability, K5=MTU |

---

## VPN Technologies

| Technology | Layer | Encryption | Multicast | Use Case |
|------------|-------|------------|-----------|----------|
| GRE | 3 | No | Yes | Basic tunneling |
| IPsec | 3 | Yes | No | Secure tunnels |
| GRE+IPsec | 3 | Yes | Yes | Enterprise VPN |
| DMVPN | 3 | Yes | Yes | Hub-spoke+spoke-spoke |
| VXLAN | 2 | No | No | Data center overlay |

---

## SD Technologies

| Technology | Component | Function |
|------------|-----------|----------|
| **SD-Access** | DNA Center | Management, policy |
| | ISE | Identity, SGT |
| | Fabric (LISP+VXLAN) | Overlay transport |
| **SD-WAN** | vManage | Management GUI |
| | vSmart | Control plane, OMP |
| | vBond | Orchestration |
| | vEdge/cEdge | Data plane |

---

## Security Quick Reference

### CoPP Classes (Priority Order)
1. Routing protocols (BGP, OSPF, EIGRP)
2. Network management (SSH, SNMP)
3. Interactive (ping, traceroute)
4. Default (everything else)

### 802.1X Order
```
dot1x → mab → webauth
```

### TrustSec Flow
```
Classification → Propagation → Enforcement
(ISE/Static)    (Inline/SXP)   (SGACL)
```

---

## Automation Protocols

| Protocol | Port | Format | Use |
|----------|------|--------|-----|
| NETCONF | 830 (SSH) | XML | Config/State |
| RESTCONF | 443 (HTTPS) | JSON/XML | REST API |
| gNMI | 50051 | Protobuf | Telemetry |
| SNMP | 161/162 | Binary | Monitoring |

---

## Key Commands

### BGP
```
show bgp summary
show bgp ipv4 unicast
show bgp ipv4 unicast neighbors
neighbor X.X.X.X route-map NAME in/out
```

### EIGRP
```
show ip eigrp neighbors
show ip eigrp topology
show ip eigrp topology all-links
variance X
```

### DMVPN
```
show dmvpn
show ip nhrp
show crypto session
```

### NETCONF/RESTCONF
```
show netconf-yang sessions
show platform software yang-management process
```

---

*Print and keep handy during labs!*

