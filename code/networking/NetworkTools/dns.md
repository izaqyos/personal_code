# DNS Tools 🔍

> **dig, nslookup, host, and DNS troubleshooting**

## dig (Domain Information Groper)

The most powerful DNS query tool.

### Basic Queries

```bash
# Simple lookup (A record)
dig example.com

# Short answer only
dig +short example.com

# Specific record types
dig example.com A        # IPv4 address
dig example.com AAAA     # IPv6 address
dig example.com MX       # Mail servers
dig example.com NS       # Name servers
dig example.com TXT      # Text records
dig example.com SOA      # Start of Authority
dig example.com CNAME    # Canonical name
dig example.com ANY      # All records (limited support)

# Reverse lookup (PTR)
dig -x 8.8.8.8
dig -x 2001:4860:4860::8888
```

### Query Specific Server

```bash
# Use specific DNS server
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Query root servers
dig @a.root-servers.net . NS
```

### Advanced Options

```bash
# Show full query process (+trace)
dig +trace example.com

# Show all sections
dig +noall +answer example.com

# Query with TCP (instead of UDP)
dig +tcp example.com

# Set timeout
dig +time=5 example.com

# Disable recursion
dig +norecurse example.com

# DNSSEC validation
dig +dnssec example.com
dig +sigchase example.com

# Show query time and server
dig +stats example.com
```

### Output Sections

```
; <<>> DiG 9.16.1 <<>> example.com
;; QUESTION SECTION:        ← What was asked
;example.com.   IN  A

;; ANSWER SECTION:          ← The response
example.com.  86400  IN  A  93.184.216.34

;; AUTHORITY SECTION:       ← Authoritative servers
example.com.  86400  IN  NS  a.iana-servers.net.

;; ADDITIONAL SECTION:      ← Extra helpful info
a.iana-servers.net. 86400 IN A 199.43.135.53

;; Query time: 45 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; MSG SIZE  rcvd: 150
```

---

## nslookup

Interactive and non-interactive DNS queries.

### Non-Interactive Mode

```bash
# Basic lookup
nslookup example.com

# Use specific server
nslookup example.com 8.8.8.8

# Query specific record type
nslookup -type=MX example.com
nslookup -type=NS example.com
nslookup -type=TXT example.com

# Reverse lookup
nslookup 8.8.8.8
```

### Interactive Mode

```bash
$ nslookup
> server 8.8.8.8
> set type=MX
> example.com
> set type=A
> www.example.com
> exit
```

---

## host

Simple, quick DNS lookups.

```bash
# Basic lookup
host example.com

# Verbose output
host -v example.com

# Specific type
host -t MX example.com
host -t NS example.com
host -t AAAA example.com

# Reverse lookup
host 8.8.8.8

# Use specific server
host example.com 8.8.8.8

# Show all records
host -a example.com
```

---

## whois

Domain registration information.

```bash
# Domain info
whois example.com

# IP address info
whois 8.8.8.8

# Specific whois server
whois -h whois.verisign-grs.com example.com
```

---

## Common DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | 93.184.216.34 |
| AAAA | IPv6 address | 2606:2800:220:1:248:1893:25c8:1946 |
| CNAME | Alias | www → example.com |
| MX | Mail server | 10 mail.example.com |
| NS | Name server | ns1.example.com |
| TXT | Text/verification | "v=spf1 include:_spf.google.com ~all" |
| SOA | Zone authority | Serial, refresh, retry, expire |
| PTR | Reverse (IP→name) | 34.216.184.93.in-addr.arpa |
| SRV | Service location | _ldap._tcp.example.com |
| CAA | Certificate authority | 0 issue "letsencrypt.org" |

---

## DNS Troubleshooting

### Check DNS Resolution Chain

```bash
# Full trace from root to answer
dig +trace example.com

# Check authoritative servers
dig NS example.com
dig @ns1.example.com example.com
```

### Check DNS Propagation

```bash
# Query multiple public DNS
for dns in 8.8.8.8 1.1.1.1 9.9.9.9 208.67.222.222; do
    echo "=== $dns ==="
    dig @$dns +short example.com
done
```

### Test DNS Server Response Time

```bash
# Time queries
for i in {1..5}; do
    dig @8.8.8.8 example.com | grep "Query time"
done
```

### Check DNSSEC

```bash
# Verify DNSSEC
dig +dnssec example.com
delv @8.8.8.8 example.com

# Check DS records
dig DS example.com
```

### Common Issues

| Issue | Check | Solution |
|-------|-------|----------|
| NXDOMAIN | Domain exists? | Verify spelling |
| SERVFAIL | Server issue | Try different DNS |
| Timeout | Connectivity | Check firewall/UDP 53 |
| Wrong answer | Caching | Wait for TTL or flush |
| No recursion | Server config | Use recursive DNS |

### Flush DNS Cache

```bash
# Linux (systemd-resolved)
sudo systemd-resolve --flush-caches

# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns
```

---

*Next: [nmap →](./nmap.md)*

