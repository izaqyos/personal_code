#!/usr/bin/env node

function isPrivateIPv6(ipAddress) {
    const ulaPrefix = /^fc|fd/i;
    const linkLocalPrefix = /^fe80/i;

    function expandIPv6(ip) {
        try {
            let parts = ip.split("::");
            if (parts.length > 2) {
                return null;
            }

            let [left, right] = parts;
            let leftSegments = left ? left.split(":") : [];
            let rightSegments = right ? right.split(":") : [];

            // Handle IPv4-mapped IPv6 addresses
            if (rightSegments.length > 0 && rightSegments[rightSegments.length - 1].includes('.')) {
                const ipv4 = rightSegments.pop();
                const ipv4parts = ipv4.split('.').map(Number);

                if (ipv4parts.length !== 4 || ipv4parts.some(part => isNaN(part) || part < 0 || part > 255)) {
                    return null;
                }

                const ipv4Hex1 = ipv4parts[0].toString(16).padStart(2, '0') + ipv4parts[1].toString(16).padStart(2, '0');
                const ipv4Hex2 = ipv4parts[2].toString(16).padStart(2, '0') + ipv4parts[3].toString(16).padStart(2, '0');
                rightSegments.push(ipv4Hex1);
                rightSegments.push(ipv4Hex2);
            }
            if (leftSegments.some(seg => seg.length > 4) || rightSegments.some(seg => seg.length > 4)) {
               return null;
            }
            const totalSegments = leftSegments.length + rightSegments.length;
            if (totalSegments > 8) {
                return null; // The critical check *before* expansion
            }

            const missingSegments = 8 - totalSegments;
            // Correctly create the expanded parts array
            let expandedParts = [];
            for (const seg of leftSegments) {
              expandedParts.push(seg.padStart(4, '0'));
            }
            for (let i = 0; i < missingSegments; i++) {
                expandedParts.push("0000");
            }
            for (const seg of rightSegments) {
              expandedParts.push(seg.padStart(4, '0'));
            }


           if (expandedParts.length !== 8 || !expandedParts.every(seg => /^[0-9a-fA-F]{4}$/.test(seg))){
                return null;
            }

            return expandedParts.join(":"); // No need to reconstruct

        } catch (e) {
            return null;
        }
    }

    ipAddress = ipAddress.trim();
    if (!ipAddress) {
        return null;
    }

    if (!/^[0-9a-fA-F:.]+$/.test(ipAddress)) {
        return null;
    }

    let expandedIp = expandIPv6(ipAddress);

    if (expandedIp === null) {
        return null;
    }

    const isULA = ulaPrefix.test(expandedIp);
    const isLinkLocal = linkLocalPrefix.test(expandedIp);

    return {
        isULA: isULA,
        isLinkLocal: isLinkLocal,
        isPrivate: isULA || isLinkLocal,
    };
}
const testCases = [
    // Valid ULAs
    { ip: "fd12:3456:789a:1::1", expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: "fd12:3456:789a:1::", expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: "fd12:3456:789a:1:1:1:1:1", expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: "fd00::", expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: "fdf0:a0b1:c2d3:1::", expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: "fc00::1", expected: { isULA: true, isLinkLocal: false, isPrivate: true } }, // Technically ULA, but discouraged
    { ip: "FC00::1", expected: { isULA: true, isLinkLocal: false, isPrivate: true } }, // Uppercase test
    { ip: 'fd12:0:0:0:0:0:0:1', expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: 'fd12::1', expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: 'fcab::1', expected: { isULA: true, isLinkLocal: false, isPrivate: true } },
    { ip: 'fca9:ffff:ffff:ffff:ffff:ffff:ffff:ffff', expected: { isULA: true, isLinkLocal: false, isPrivate: true } },

    // Valid Link-Local
    { ip: "fe80::1", expected: { isULA: false, isLinkLocal: true, isPrivate: true } },
    { ip: "fe80::20c:29ff:fe12:3456", expected: { isULA: false, isLinkLocal: true, isPrivate: true } },
    { ip: "FE80::1", expected: { isULA: false, isLinkLocal: true, isPrivate: true } }, // Uppercase test
    { ip: "fe80::", expected: { isULA: false, isLinkLocal: true, isPrivate: true } },
    { ip: 'fe80:0:0:0:0:0:0:1', expected: { isULA: false, isLinkLocal: true, isPrivate: true } },
    { ip: 'fe80::1', expected: { isULA: false, isLinkLocal: true, isPrivate: true } },
    { ip: 'fe80::ffff:ffff:ffff:ffff', expected: { isULA: false, isLinkLocal: true, isPrivate: true } },

    // Global Unicast (not private)
    { ip: "2001:db8::1", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },
    { ip: "2001:0db8::", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },
    { ip: "2600:1f14:c81:5900:14ac:a12b:a605:abcd", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },
    { ip: "2001:db8:85a3::8a2e:370:7334", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },
    { ip: "2001:4860:4860::8888", expected: { isULA: false, isLinkLocal: false, isPrivate: false } }, // Google DNS
    { ip: "2001:4860:4860::8844", expected: { isULA: false, isLinkLocal: false, isPrivate: false } }, // Google DNS
    { ip: "::ffff:192.0.2.128", expected: { isULA: false, isLinkLocal: false, isPrivate: false } }, //IPv4 mapped

    // Loopback
    { ip: "::1", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },

    // Multicast
    { ip: "ff02::1", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },
    { ip: "ff02::1:ff00:1", expected: { isULA: false, isLinkLocal: false, isPrivate: false } },

    // Invalid IPv6
    { ip: "192.168.1.1", expected: null },  // IPv4
    { ip: "invalid", expected: null },
    { ip: "fd12:3456:789a:1::1:2", expected: null }, // Too many segments
    { ip: "fe80::20c:29ff:fe12:3456:12345", expected: null }, // Invalid hextet
    { ip: "fe80::20c:29ff:fe12:345g", expected: null },  // Invalid character
    { ip: "fe80::20c:29ff:fe12:", expected: null },
    { ip: "fdxy::1", expected: null },  // Invalid characters in prefix
    { ip: "", expected: null }, // Empty
    { ip: " ", expected: null }, // Whitespace
    { ip: ":", expected: null },
    { ip: ":::", expected: null },
    { ip: "2001:db8::1::1", expected: null },
    { ip: 'fd12:3456:789a:1:1:1:1:1:1', expected: null }, //Too long
    { ip: 'fe80:1:1:1:1:1:1:1:1', expected: null },//Too long
    { ip: '2001:db8:::1', expected: null }, // Multiple ::
];

function runTests() {
    let allTestsPassed = true;
    let failedTests = 0;
    const numTests = testCases.length;

    for (let i = 0; i < numTests; i++) {
        const test = testCases[i];
        const result = isPrivateIPv6(test.ip);
        const testNumber = i + 1;

        if (JSON.stringify(result) !== JSON.stringify(test.expected)) {
            allTestsPassed = false;
            failedTests++;
            console.error(`Test ${testNumber} FAILED: Input: ${test.ip}`);
            console.error(`  Expected:`, test.expected);
            console.error(`  Actual:`, result);
        }
    }

    if (allTestsPassed) {
        console.log(`\nAll ${numTests} tests PASSED!`);
    } else {
        console.error(`\n${failedTests} out of ${numTests} tests FAILED!`);
        process.exit(1); // Exit with a non-zero code to indicate failure
    }
}
runTests();
