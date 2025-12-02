# CCNA Refresher Course 🌐

> **A comprehensive refresher for experienced network professionals returning to CCNA material**

## 📋 Overview

This project is designed for someone who completed CCNA training ~11 years ago and needs to refresh their knowledge while catching up with the modern CCNA curriculum (200-301). The current CCNA consolidates the old CCNA Routing & Switching, Security, Cloud, and Wireless tracks into one comprehensive certification.

### What's Changed Since Your Last CCNA?

| Then (Pre-2020)                    | Now (CCNA 200-301)                           |
| ---------------------------------- | -------------------------------------------- |
| Multiple CCNA tracks               | Single consolidated CCNA                     |
| RIP, EIGRP, OSPF routing           | Focus on OSPF (single-area & multi-area)     |
| Basic switching                    | Advanced VLAN, STP, EtherChannel             |
| Minimal automation                 | **Network Automation & Programmability** 🆕  |
| CLI-only management                | REST APIs, JSON, YAML, Ansible, Python       |
| Traditional data centers           | **SDN & Controller-based architecttic** 🆕   |
| IPv4 primary focus                 | IPv6 parity (dual-stack mandatory)           |
| Basic security                     | Zero Trust, Threat defense, MFA              |
| Physical networking only           | Wireless fundamenttic (802.11, WLCs)         |

## 🗂️ Project Structure

```
CCNA/
├── README.md                    # This file
├── ROADMAP.md                   # Learning path & time estimates
├── PROGRESS.md                  # ✅ Track your progress (pause/resume)
│
├── modules/
│   ├── 01-network-fundamentals/ # OSI, TCP/IP, IPv4/IPv6, cables
│   ├── 02-network-access/       # VLANs, STP, EtherChannel, Wireless
│   ├── 03-ip-connectivity/      # Routing, OSPF, static routes
│   ├── 04-ip-services/          # NAT, DHCP, DNS, NTP, QoS
│   ├── 05-security/             # ACLs, port security, AAA
│   └── 06-automation/           # APIs, SDN, Python, Ansible 🆕
│
├── exercises/
│   ├── packet-tracer/           # Cisco Packet Tracer labs
│   ├── cli-drills/              # Command practice exercises
│   └── troubleshooting/         # Scenario-based troubleshooting
│
├── cheatsheets/                 # Quick reference cards
└── practice-exams/              # Self-assessment quizzes
```

## 🚀 Getting Started

### Prerequisites

1. **Cisco Packet Tracer** (free with Cisco NetAcad account)
   - Download: https://www.netacad.com/courses/packet-tracer
   
2. **GNS3** (optional, for more realistic labs)
   - Download: https://www.gns3.com/
   
3. **Python 3.x** (for automation module)
   ```bash
   python3 --version  # Should be 3.8+
   ```

### Recommended Study Schedule

| Experience Level        | Daily Time | Est. Completion |
| ----------------------- | ---------- | --------------- |
| Quick Refresh           | 1-2 hours  | 4-6 weeks       |
| Thorough Review         | 2-3 hours  | 8-10 weeks      |
| Exam Preparation        | 3-4 hours  | 12-16 weeks     |

## 📖 How to Use This Course

1. **Start with ROADMAP.md** - Review the learning path
2. **Update PROGRESS.md** - Check off completed topics
3. **Work through modules sequentially** - Build on fundamentals
4. **Complete exercises after each module** - Hands-on reinforcement
5. **Use cheatsheets for review** - Quick reference during labs

## 🎯 Learning Objectives

After completing this refresher, you will be able to:

- [ ] Configure and troubleshoot VLANs, STP, and EtherChannel
- [ ] Implement single-area and multi-area OSPF
- [ ] Configure IPv4 and IPv6 addressing schemes
- [ ] Implement NAT, DHCP, and DNS services
- [ ] Apply security best practices (ACLs, port security, AAA)
- [ ] **Understand network automation with Python and REST APIs** 🆕
- [ ] **Work with SDN controllers and Cisco DNA Center** 🆕
- [ ] Configure and troubleshoot wireless networks

## 📚 Additional Resources

### Official Cisco Resources
- [CCNA Exam Topics](https://www.cisco.com/c/en/us/training-events/training-certifications/exams/current-list/ccna-200-301.html)
- [Cisco Learning Network](https://learningnetwork.cisco.com/)

### Recommended Books
- *CCNA 200-301 Official Cert Guide* - Wendell Odom
- *31 Days Before Your CCNA Exam* - Allan Johnson

### Video Courses
- Jeremy's IT Lab (YouTube - free)
- David Bombal (Udemy)
- CBT Nuggets (paid)

### Practice Labs
- [Cisco Modeling Labs](https://developer.cisco.com/modeling-labs/)
- [EVE-NG](https://www.eve-ng.net/)

## ⚡ Quick Start Commands

```bash
# Navigate to the project
cd ~/work/git/personal_code/code/networking/CCNA

# Open progress tracker
cat PROGRESS.md

# Start with Module 1
cd modules/01-network-fundamentals
```

---

**Good luck with your refresher!** 🎓

*Last updated: December 2025*

