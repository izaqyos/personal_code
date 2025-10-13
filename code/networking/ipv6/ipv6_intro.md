# IPv6 Tutorial: From Basics to Advanced Concepts

This tutorial covers IPv6 (Internet Protocol version 6), the successor to IPv4. It's designed to be comprehensive, starting with fundamental concepts and progressing to more advanced topics.

## Table of Contents

1.  **Why IPv6? (The Limitations of IPv4)**
2.  **IPv6 Address Structure and Notation**
    *   Hexadecimal Representation
    *   Zero Compression
    *   Leading Zero Suppression
3.  **IPv6 Address Types**
    *   Unicast (Global Unicast, Link-Local, Unique Local, IPv4-Mapped)
    *   Multicast
    *   Anycast
4.  **IPv6 Header Format**
5.  **Stateless Address Autoconfiguration (SLAAC)**
6.  **Neighbor Discovery Protocol (NDP)**
    *   Router Solicitation (RS) and Router Advertisement (RA)
    *   Neighbor Solicitation (NS) and Neighbor Advertisement (NA)
    *   Duplicate Address Detection (DAD)
7.  **DHCPv6**
8.  **IPv6 and DNS**
    *   AAAA Records
    *   Reverse DNS (ip6.arpa)
9.  **Transition Mechanisms**
    *   Dual Stack
    *   Tunneling (6to4, Teredo, ISATAP)
    *   NAT64
10. **IPv6 Security Considerations**
    *   IPsec (built-in, but not always used)
    *   Firewall Rules
    *   Privacy Extensions
11. **Advanced Topics**
    *   Mobile IPv6
    *   Routing Protocols (RIPng, OSPFv3, BGP-4+)
    *   IPv6 Extension Headers
    *   Multicast Listener Discovery (MLD)
12. **Example Configurations (brief)**

## 1. Why IPv6? (The Limitations of IPv4)

IPv4, the current version of the Internet Protocol, uses 32-bit addresses. This provides approximately 4.3 billion unique addresses (2<sup>32</sup>). While this seemed like a vast number initially, the rapid growth of the internet and the proliferation of internet-connected devices (IoT, smartphones, etc.) have led to IPv4 address exhaustion.  Network Address Translation (NAT) was a workaround, but it introduced complexities and limitations.

IPv6 was designed to solve this problem with:

*   **Vastly Larger Address Space:** IPv6 uses 128-bit addresses, providing an almost unimaginable number of addresses (2<sup>128</sup> or approximately 3.4 x 10<sup>38</sup>).  This eliminates the need for NAT in most cases.
*   **Simplified Header:** The IPv6 header is simpler than the IPv4 header, leading to more efficient processing by routers.
*   **Built-in Autoconfiguration:** IPv6 devices can configure their own addresses automatically, reducing administrative overhead.
*   **Integrated Security:** IPsec (Internet Protocol Security) is an integral part of IPv6 (although its *use* is not mandatory).
*   **Improved Multicast:** More efficient multicast support.
*   **Anycast Support:**  Allows sending data to the "nearest" of several possible destinations.

## 2. IPv6 Address Structure and Notation

IPv6 addresses are 128 bits long, represented in hexadecimal notation.  They are divided into eight groups of 16 bits (two bytes, or four hexadecimal characters) each, separated by colons.

*   **Hexadecimal Representation:** Each group represents 16 bits, written as four hexadecimal digits (0-9, a-f).

    Example: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

*   **Zero Compression:** Consecutive groups of all zeros can be replaced by a *single* double colon (`::`).  This can only be done *once* in an address to avoid ambiguity.

    Example:  `2001:0db8:85a3:0000:0000:8a2e:0370:7334`  can be shortened to  `2001:0db8:85a3::8a2e:0370:7334`

    Another Example: `2001:db8::1` (short for `2001:0db8:0000:0000:0000:0000:0000:0001`)

    Invalid Example: `2001::db8::1` (ambiguous - which groups are zeros?)

*   **Leading Zero Suppression:** Leading zeros *within* a 16-bit group can be omitted.

    Example: `2001:0db8:85a3:0000:0000:8a2e:0370:7334` can be written as `2001:db8:85a3:0:0:8a2e:370:7334` (and further compressed with `::`)

**Combined Example:**

`2001:0db8:0000:0000:0000:0000:0000:0001` becomes `2001:db8::1`

**IPv4-Mapped IPv6 Addresses:**

A special notation exists for representing IPv4 addresses within an IPv6 address.  The last 32 bits are written in dotted-decimal IPv4 notation.

Example: `::ffff:192.168.1.1`  (This is an IPv6 address that "wraps" an IPv4 address)

## 3. IPv6 Address Types

*   **Unicast:**  Identifies a *single* interface.  A packet sent to a unicast address is delivered to that specific interface.
    *   **Global Unicast:**  Globally routable addresses, similar to public IPv4 addresses.  They typically start with `2000::/3` (meaning the first three bits are 001).  Example: `2001:db8::1`
    *   **Link-Local:**  Used for communication *within* a single network segment (link).  They are *not* routable.  All link-local addresses start with `fe80::/10`.  They are automatically configured on all IPv6 interfaces. Example: `fe80::1`
    *   **Unique Local (ULA):**  Similar to private IPv4 addresses (like 192.168.x.x).  They are intended for use within a site or organization and are not supposed to be globally routable, although in practice, strict enforcement is difficult.  ULAs start with `fc00::/7`. Example: `fd12:3456:789a:1::1`
    *   **IPv4-Mapped:** Used to represent IPv4 addresses within an IPv6 address (for transition mechanisms).  Example: `::ffff:192.168.1.1`
    *   **Loopback:** The address `::1` (0000:0000:0000:0000:0000:0000:0000:0001) is the loopback address.  It is the equivalent of 127.0.0.1 in IPv4.
    *   **Unspecified Address:** The address `::` (all zeros) is the unspecified address. It's used in certain configuration scenarios (e.g., as a placeholder source address when a device hasn't yet acquired its address).  It's not a valid unicast address for normal communication.

*   **Multicast:**  Identifies a *group* of interfaces. A packet sent to a multicast address is delivered to *all* interfaces in that group.  Multicast addresses start with `ff`.  Example: `ff02::1` (all nodes on the local link).

*   **Anycast:** Identifies a *set* of interfaces, but a packet sent to an anycast address is delivered to only *one* of those interfaces (typically the "nearest" one, according to the routing protocol).  Anycast addresses are taken from the unicast address space; there's no special prefix.

## 4. IPv6 Header Format

The IPv6 header is simpler than the IPv4 header. It has a fixed size of 40 bytes.

| Field             | Size (bits) | Description                                                                                                                                   |
| ----------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Version           | 4           | IP version (always 6 for IPv6).                                                                                                                |
| Traffic Class     | 8           | Similar to IPv4's Type of Service (ToS) field. Used for Quality of Service (QoS).                                                             |
| Flow Label        | 20          | Used to identify packets belonging to the same flow (for QoS and performance).                                                               |
| Payload Length    | 16          | Length of the data portion of the packet (excluding the header) in bytes.                                                                      |
| Next Header       | 8           | Identifies the type of the next header (e.g., TCP, UDP, ICMPv6, or an extension header).                                                   |
| Hop Limit         | 8           | Similar to IPv4's Time to Live (TTL). Decremented by each router; packet is discarded if it reaches 0.                                        |
| Source Address    | 128         | IPv6 address of the sender.                                                                                                                 |
| Destination Address | 128         | IPv6 address of the recipient.                                                                                                               |

**Key Differences from IPv4:**

*   **No Header Checksum:** IPv6 relies on upper-layer protocols (like TCP and UDP) and link-layer protocols for error detection. This simplifies header processing.
*   **No Fragmentation in the Header:** Fragmentation is handled by the *source* host, not by routers.  This improves routing efficiency.  Path MTU Discovery (PMTUD) is used to determine the maximum packet size.
*   **No Options Field (usually):**  Optional information is carried in *extension headers*, which are placed *after* the main IPv6 header and *before* the upper-layer protocol header (like TCP or UDP).

## 5. Stateless Address Autoconfiguration (SLAAC)

SLAAC is a key feature of IPv6 that allows devices to automatically configure their own addresses without a DHCP server.  Here's how it works:

1.  **Link-Local Address Generation:** When an IPv6 interface is enabled, it automatically generates a link-local address. This is usually done by combining the `fe80::/10` prefix with a modified EUI-64 identifier (derived from the interface's MAC address).  There are privacy extensions that randomize this part.
2.  **Duplicate Address Detection (DAD):** The device sends a Neighbor Solicitation (NS) message to its own link-local address to ensure it's unique on the link.  If it receives a Neighbor Advertisement (NA) in response, the address is a duplicate, and the process must be restarted (usually with a different interface identifier).
3.  **Router Solicitation (RS):** The device sends a Router Solicitation (RS) message to the all-routers multicast address (`ff02::2`). This asks any routers on the link to identify themselves.
4.  **Router Advertisement (RA):** Routers on the link respond with Router Advertisement (RA) messages. These messages contain:
    *   **Prefix Information:**  One or more /64 prefixes that the device can use to create global unicast addresses.
    *   **Default Gateway:** The link-local address of the router.
    *   **Other Information:** DNS server addresses, MTU, etc.
5.  **Global Address Generation:** The device combines a prefix from the RA with its interface identifier (often a modified EUI-64 or a randomly generated identifier for privacy) to create a global unicast address.
6.  **DAD (again):** The device performs DAD on its newly created global address.

## 6. Neighbor Discovery Protocol (NDP)

NDP is a fundamental protocol in IPv6, replacing several IPv4 protocols (ARP, ICMP Router Discovery, and ICMP Redirect). NDP uses ICMPv6 messages.

*   **Router Solicitation (RS) - ICMPv6 type 133:**  Sent by hosts to find routers on the link.
*   **Router Advertisement (RA) - ICMPv6 type 134:** Sent by routers to announce their presence and provide network configuration information (prefixes, default gateway, etc.).
*   **Neighbor Solicitation (NS) - ICMPv6 type 135:**  Used for address resolution (like ARP in IPv4) and Duplicate Address Detection (DAD).
*   **Neighbor Advertisement (NA) - ICMPv6 type 136:** Sent in response to an NS, or proactively to update neighbors about address changes.
*   **Redirect - ICMPv6 type 137:**  Used by routers to inform hosts of a better next-hop router for a particular destination.

**Address Resolution (like ARP in IPv4):**

1.  **Host A wants to send a packet to Host B on the same link.** Host A knows Host B's IPv6 address, but needs Host B's MAC address.
2.  **Host A sends a Neighbor Solicitation (NS).** The NS is sent to the *solicited-node multicast address* of Host B. This multicast address is derived from Host B's unicast address.
3.  **Host B receives the NS.** Because Host B is part of the solicited-node multicast group, it receives the NS.
4.  **Host B replies with a Neighbor Advertisement (NA).** The NA contains Host B's MAC address.
5.  **Host A receives the NA and can now send packets directly to Host B.**

**Duplicate Address Detection (DAD):**

1.  A device generates a tentative IPv6 address (link-local or global).
2.  It sends a Neighbor Solicitation (NS) message to that tentative address.
3.  If it receives a Neighbor Advertisement (NA) in response, the address is a duplicate.
4.  If it receives no NA after a short time, the address is considered unique.

## 7. DHCPv6

While SLAAC is a powerful feature, DHCPv6 (Dynamic Host Configuration Protocol for IPv6) still exists and can be used.  There are two main modes:

*   **Stateless DHCPv6:**  Used to provide configuration information *other than* addresses (e.g., DNS server addresses, domain name).  Devices still use SLAAC for address configuration.
*   **Stateful DHCPv6:** Similar to DHCP in IPv4.  The DHCPv6 server assigns and manages IPv6 addresses, and can also provide other configuration information.

## 8. IPv6 and DNS

*   **AAAA Records:**  Used to map a hostname to an IPv6 address (similar to A records for IPv4).  Example: `example.com.  AAAA  2001:db8::1`
*   **Reverse DNS (ip6.arpa):**  Used to map an IPv6 address back to a hostname.  The IPv6 address is reversed, nibble by nibble (4 bits), and appended to `.ip6.arpa.`.  Example: The reverse lookup for `2001:db8::1` would involve querying for `1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa.`

## 9. Transition Mechanisms

Since the transition from IPv4 to IPv6 is gradual, several mechanisms exist to allow IPv6 and IPv4 networks to interoperate:

*   **Dual Stack:**  Devices run both IPv4 and IPv6 simultaneously.  This is the preferred long-term solution.
*   **Tunneling:**  Encapsulates IPv6 packets within IPv4 packets (or vice-versa) to traverse networks that don't support the other protocol.
    *   **6to4:**  Allows isolated IPv6 networks to communicate over an IPv4 internet without explicit tunnel configuration.  Uses a special address prefix (`2002::/16`).
    *   **Teredo:**  Allows IPv6 connectivity behind IPv4 NATs.  Uses UDP encapsulation.
    *   **ISATAP (Intra-Site Automatic Tunnel Addressing Protocol):**  Used to connect IPv6 hosts within an IPv4 network.
*   **NAT64:**  Allows IPv6-only hosts to communicate with IPv4-only servers.  Translates IPv6 addresses to IPv4 addresses (and vice-versa).  Requires a pool of public IPv4 addresses.

## 10. IPv6 Security Considerations

*   **IPsec:**  IPsec is integrated into IPv6, providing encryption and authentication.  However, its *use* is not mandatory, so you still need to configure it.
*   **Firewall Rules:**  IPv6 requires different firewall rules than IPv4.  You need to allow ICMPv6 traffic for NDP to function correctly.
*   **Privacy Extensions:**  SLAAC originally used the MAC address to generate the interface identifier portion of an IPv6 address. This could lead to privacy concerns (tracking a device across networks).  Privacy extensions generate random interface identifiers, making tracking more difficult.

## 11. Advanced Topics

*   **Mobile IPv6 (MIPv6):** Allows mobile devices to maintain a permanent IPv6 address ("home address") while roaming to different networks.
*   **Routing Protocols:**
    *   **RIPng:**  Routing Information Protocol next generation (for IPv6).
    *   **OSPFv3:** Open Shortest Path First version 3 (for IPv6).
    *   **BGP-4+:** Border Gateway Protocol (with multiprotocol extensions for IPv6).
*   **IPv6 Extension Headers:**  Used to carry optional information.  Examples