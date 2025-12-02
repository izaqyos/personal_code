# CCNP Exercises & Labs 🔬

> **Advanced hands-on practice for CCNP ENCOR**

## Lab Requirements

CCNP labs require more sophisticated environments than CCNA:

### Recommended Platforms

| Platform | Use Case | Notes |
|----------|----------|-------|
| EVE-NG | Full labs | Community or Pro |
| Cisco CML | Official | $199/year personal |
| GNS3 | Routing-focused | Free |
| DevNet Sandbox | API/Automation | Free (limited time) |

### Required Images

- IOSv (routing)
- IOSvL2 (switching)
- CSR1000v (IOS-XE)
- vWLC (wireless)
- ISE (identity services)

---

## Lab Categories

### 🛣️ Infrastructure Labs (30% exam weight)

| Lab | Topics | Time |
|-----|--------|------|
| EIGRP Advanced | Named mode, stub, summarization | 2 hr |
| OSPF Multi-Area | LSA types, areas, filtering | 3 hr |
| BGP Fundamentals | eBGP/iBGP, path selection | 3 hr |
| BGP Path Manipulation | Weight, LP, AS-path, MED | 2 hr |
| Route Redistribution | OSPF ↔ EIGRP, loop prevention | 2 hr |
| Multicast | PIM-SM, RP, IGMP | 2 hr |

### 🌐 Virtualization Labs (20% exam weight)

| Lab | Topics | Time |
|-----|--------|------|
| VRF-Lite | Multiple VRFs, route leaking | 2 hr |
| GRE Tunnels | Basic GRE, GRE over IPsec | 1.5 hr |
| IPsec VPN | Site-to-site IKEv2 | 2 hr |
| DMVPN | Phase 2/3, NHRP, spoke-to-spoke | 3 hr |
| LISP | xTR, MS/MR configuration | 2 hr |

### 🔐 Security Labs (20% exam weight)

| Lab | Topics | Time |
|-----|--------|------|
| CoPP | Traffic classification, policing | 1.5 hr |
| 802.1X | Dot1x, MAB, ISE integration | 2 hr |
| MACsec | Switch-to-switch encryption | 1 hr |
| Infrastructure Hardening | AAA, SSH, uRPF | 1.5 hr |

### 📊 Assurance Labs (10% exam weight)

| Lab | Topics | Time |
|-----|--------|------|
| NetFlow | Flexible NetFlow, collectors | 1 hr |
| SPAN/ERSPAN | Local, remote, encapsulated | 1 hr |
| IP SLA | Probes, tracking, failover | 1 hr |

### 🤖 Automation Labs (10% exam weight)

| Lab | Topics | Time |
|-----|--------|------|
| Python + Netmiko | Device interaction, config backup | 1.5 hr |
| NETCONF | ncclient, YANG models | 2 hr |
| RESTCONF | REST API operations | 1.5 hr |
| Ansible | Playbooks, templates, inventory | 2 hr |
| DNA Center API | Authentication, device queries | 1.5 hr |
| EEM | Applets, event-driven automation | 1 hr |

---

## Sample Lab: DMVPN Phase 3

### Topology

```
                        ┌──────────────┐
                        │     Hub      │
                        │ 203.0.113.1  │
                        │  10.0.0.1    │
                        └──────┬───────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
    ┌──────┴───────┐    ┌──────┴───────┐    ┌──────┴───────┐
    │   Spoke1     │    │   Spoke2     │    │   Spoke3     │
    │198.51.100.1  │    │198.51.100.2  │    │198.51.100.3  │
    │  10.0.0.2    │    │  10.0.0.3    │    │  10.0.0.4    │
    └──────────────┘    └──────────────┘    └──────────────┘
           │                   │                   │
      192.168.1.0/24     192.168.2.0/24     192.168.3.0/24
```

### Objectives

1. Configure DMVPN hub with mGRE
2. Configure DMVPN spokes
3. Add IPsec encryption
4. Configure EIGRP over DMVPN
5. Verify spoke-to-spoke tunnels (Phase 3)

### Verification Commands

```cisco
show dmvpn
show ip nhrp
show crypto session
show ip route eigrp
```

---

## Lab Tips

1. **Save states** - Snapshot your VMs before major changes
2. **Document** - Keep notes on what worked
3. **Break it** - Intentionally misconfigure to practice troubleshooting
4. **Time yourself** - Build speed for the exam
5. **Use Wireshark** - Capture and analyze protocol behavior

---

## Free Lab Resources

- [Cisco DevNet Sandboxes](https://developer.cisco.com/site/sandbox/)
- [EVE-NG Community](https://www.eve-ng.net/)
- [GNS3 Academy](https://academy.gns3.com/)

---

*Back to: [CCNP README](../README.md)*

