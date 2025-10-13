
// test node --test
// url-validator.js
import { URL, domainToASCII } from 'node:url';
import dns from 'node:dns/promises';
import net from 'node:net';
import ipaddr from 'ipaddr.js';

const ALLOWED_SCHEMES = new Set(['https', 'http']);
const BLOCKED_HOSTNAMES = new Set(['localhost']);

// IPv4/IPv6 special/bogon-ish ranges commonly blocked for SSRF/DNS-rebinding defense
const IPV4_CIDRS = [
  '0.0.0.0/8',    // "this" network
  '10.0.0.0/8',   // private
  '100.64.0.0/10',// CGNAT
  '127.0.0.0/8',  // loopback
  '169.254.0.0/16', // link-local
  '172.16.0.0/12',  // private
  '192.0.0.0/24',   // IETF protocol assignments
  '192.0.2.0/24',   // TEST-NET-1
  '192.88.99.0/24', // 6to4 (deprecated)
  '192.168.0.0/16', // private
  '198.18.0.0/15',  // benchmarking
  '198.51.100.0/24',// TEST-NET-2
  '203.0.113.0/24', // TEST-NET-3
  '224.0.0.0/4',    // multicast
  '240.0.0.0/4',    // reserved
  '255.255.255.255/32', // broadcast
];

const IPV6_CIDRS = [
  '::/128',        // unspecified
  '::1/128',       // loopback
  '::ffff:0:0/96', // IPv4-mapped
  '64:ff9b::/96',  // NAT64 (optional block)
  '100::/64',      // discard-only
  '2001:db8::/32', // documentation
  '2001::/23',     // IETF/IANA specials umbrella
  'fc00::/7',      // ULA (private)
  'fe80::/10',     // link-local
  'ff00::/8',      // multicast
];

const BLOCKED_NETS = [
  ...IPV4_CIDRS.map(c => ({ family: 4, net: ipaddr.parseCIDR(c) })),
  ...IPV6_CIDRS.map(c => ({ family: 6, net: ipaddr.parseCIDR(c) })),
];

function ipIsBlocked(ip) {
  const a = ipaddr.parse(ip); // throws if invalid
  return BLOCKED_NETS.some(({ family, net }) => {
    return (a.kind() === 'ipv4' && family === 4 && a.match(net)) ||
           (a.kind() === 'ipv6' && family === 6 && a.match(net));
  });
}
/*
127.0.0.1 → kind ipv4 → matches 127.0.0.0/8 → true
192.168.10.5 → kind ipv4 → matches 192.168.0.0/16 → true
8.8.8.8 → kind ipv4 → no matches → false
fe80::1 → kind ipv6 → matches fe80::/10 → true
::ffff:10.0.0.1 → kind ipv6 → matches ::ffff:0:0/96 → true (v4-mapped
*/

async function resolveAll(host) {
  const set = new Set();
  // IP literal short-circuit
  if (net.isIP(host)) return [host];
  // DNS (ignore errors; we’ll decide based on requireResolvable)
  await Promise.all([
    dns.resolve4(host).then(arr => arr.forEach(x => set.add(x))).catch(() => {}),
    dns.resolve6(host).then(arr => arr.forEach(x => set.add(x))).catch(() => {}),
  ]);
  return [...set];
}

/**
 * Validate a user-supplied URL.
 * - WHATWG URL parsing
 * - Allowed schemes
 * - Forbid userinfo
 * - Punycode hostname
 * - Resolve and block private/special/bogon IPs
 *
 * @param {string} input
 * @param {{ requireResolvable?: boolean }} [opts]
 * @returns {Promise<{ok: boolean, errors: string[], normalized?: string, host?: string, ips?: string[]}>}
 */
export async function validateUrl(input, opts = {}) {
  const { requireResolvable = true } = opts;
  const errors = [];

  // Parse
  let u;
  try {
    if (typeof URL.canParse === 'function' && !URL.canParse(input)) throw new Error();
    u = new URL(input);
  } catch {
    return { ok: false, errors: ['Invalid absolute URL'] };
  }

  // Scheme allowlist
  const scheme = u.protocol.slice(0, -1);
  if (!ALLOWED_SCHEMES.has(scheme)) errors.push('Scheme not allowed');

  // Forbid userinfo
  if (u.username || u.password) errors.push('Credentials in URL are not allowed');

  // Punycode host
  const asciiHost = domainToASCII(u.hostname).toLowerCase();
  if (!asciiHost) errors.push('Invalid hostname');
  if (BLOCKED_HOSTNAMES.has(asciiHost)) errors.push('Host is disallowed (localhost)');

  // DNS/IP checks
  let ips = [];
  if (asciiHost) {
    ips = await resolveAll(asciiHost);
    if (requireResolvable && ips.length === 0) errors.push('Host does not resolve');

    for (const ip of ips) {
      try {
        if (ipIsBlocked(ip)) {
          errors.push(`IP denied: ${ip}`);
          break;
        }
      } catch {
        errors.push(`Unparseable IP from DNS: ${ip}`);
        break;
      }
    }
  }

  const ok = errors.length === 0;
  if (ok) {
    u.hostname = asciiHost; // normalize to punycode in the final string
    return { ok, errors, normalized: u.toString(), host: asciiHost, ips };
  }
  return { ok, errors, host: asciiHost || undefined, ips };
}
