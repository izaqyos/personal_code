#!/usr/bin/env node

/**
 * Checks if a given IPv6 address is a Unique Local Address (ULA) or a Link-Local Address.
 *
 * @param {string} ipAddress The IPv6 address to check (e.g., "fd12:3456:789a:1::1", "fe80::1").
 * @returns {object} An object with boolean properties: `isULA`, `isLinkLocal`, and `isPrivate`.
 *                   `isPrivate` is true if either `isULA` or `isLinkLocal` is true.  Returns
 *                    `null` if the input is not a valid IPv6 address.
 */
function isPrivateIPv6(ipAddress) {
  // Regular expressions for ULA and Link-Local prefixes.
  const ulaRegex = /^f[cd][0-9a-f]{2}(:[0-9a-f]{1,4}){0,7}$/i; // Matches fc00::/7 and fd00::/8
  const linkLocalRegex = /^fe80(:[0-9a-f]{1,4}){0,7}$/i;

  // Helper function to expand a shortened IPv6 address to its full form.
  function expandIPv6(ip) {
    if (ip.includes("::")) {
      const parts = ip.split("::");
      const left = parts[0].split(":");
      const right = parts[1] ? parts[1].split(":") : [];
      const missing = 8 - (left.length + right.length);

      let expanded = left.join(":");
      for (let i = 0; i < missing; i++) {
        expanded += expanded.length > 0 ? ":0000" : "0000";
      }
      expanded += right.length > 0 ? ":" + right.join(":") : "";
      return expanded;

    } else {
        return ip; // No '::' to expand
    }
  }

  // 1. Basic Validation: Check if it's a *potentially* valid IPv6 address.
  if (!/^[0-9a-f:]+$/i.test(ipAddress)) {
      return null; // Invalid characters.
  }

  // 2. Expand any shortened notation (::).
   let expandedIp = expandIPv6(ipAddress);
  if(expandedIp.split(':').some(part => part.length > 4)) {
    return null; //Invalid - segment bigger than 4
  }

    const fullParts = expandedIp.split(':').map(part => part.padStart(4,'0'));
	expandedIp = fullParts.join(':');


  // 3. Check against ULA and Link-Local regexes.
  const isULA = ulaRegex.test(expandedIp);
  const isLinkLocal = linkLocalRegex.test(expandedIp);

  // 4. Return results.
  return {
    isULA: isULA,
    isLinkLocal: isLinkLocal,
    isPrivate: isULA || isLinkLocal,
  };
}

// --- CLI Script ---

// Regular expression to find potential IPv6 addresses within a string.
const ipv6Regex = /([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}|::|([0-9a-fA-F]{1,4}:){1,6}::([0-9a-fA-F]{1,4})?|([0-9a-fA-F]{1,4}:){1,7}:|:([0-9a-fA-F]{1,4}:){1,7}|([0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){0,5}::([0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,4}::([0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4})/g;

// Get the input string from command-line arguments.
const inputString = process.argv.slice(2).join(" ");

if (!inputString) {
  console.error("Error: Please provide a string as an argument.");
  console.error("Usage: node script.js \"<your string here>\"");
  process.exit(1);
}

// Find all potential IPv6 addresses in the string.
const matches = inputString.match(ipv6Regex);

if (matches) {
  matches.forEach((ip) => {
    const result = isPrivateIPv6(ip);
    if (result && result.isPrivate) {
        let type = "";
        if (result.isULA){
            type = "(ULA)";
        } else {
            type = "(Link-Local)";
        }
      console.log(`Found private IPv6 address: ${ip} ${type}`);
    }
  });
} else {
  console.log("No IPv6 addresses found in the input string.");
}
