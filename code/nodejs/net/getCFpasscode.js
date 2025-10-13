const fetch = require('node-fetch');

const response = fetch("https://login.cf.eu10.hana.ondemand.com/passcode", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,es-419;q=0.8,es;q=0.7,he;q=0.6",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "mdsoucrssfvgrgtfyoelwapmrpza=VGPqdAMvlj90akNqMX9KSC%2BgCC0%2FddpE1%2FS7lRt2ZKqGNN7QysGDgVQXwPaub%2B7MutDEm33FWTZKMCwSPehbz0jKzoQvJDtaUuz0QJk17TsBC%2BgQgm5cgDbzQNwdyPaQX8dCoF3KIRqbZM63dMhHaf%2F7sJ1ornIOt8U5BNP70xRYRWFfy0Eh6twzVgaa5Ot2Y9Q0XeZdYFtKYzZ4p4xFk6%2F%2FBuhfru8gGnwn%2FWijL2YhjmOf%2FUAuLwYGr1HmzuXBZQnmFPGnURriu3kIbWV18c7IZCKo7FKt1fvjaBKilI%2FLEdVfKRn8ZWwDrkyEu%2FaVNSsVMJIFOaFO5Cq3rJKYMz6mfYlK5fbAI8v%2BCiHcon1lYc%2FacQEZlCSaaw24l2S3iFpASB9O7UjOHHHd0Ut1tA%3D%3D; mdsoucrsthnikxnedrwhvuefpuwr=ExHTn15Ak%2B8TniHWXFj9HFftP%2BnC3oak8%2B3mHhd9WTUVEAU7ZR7EvUaLr2JF8Wvmko13a1Ufht%2BuQcNiOqRlg5mUXK%2F5QXc0BscZ1HRvTHCaa9Sbt5z1OT5wjbJnySpTFJtGa4R7znoFcCwCWnBCQlKRgajUrFmXWj8Jh8Di8OXZRiGdbvV8AWrxi08ROzLIvCCmIXj2ndBTMBObjC8D0W0iLuU14NInwbYQYN%2Fr8VCJfuVnibv6vIQ0cfOq1naWOPx6C1zS2j3%2FGQQR2MNwghe5Q%2B%2FZDjEba95R%2Fy9%2BU8cuBJcVSCaVl5pWUAAWoLGfR9Lxhrc%2FDXjfhtphJW0tuNvWZn%2F%2BOgQxZ6YFluM25E1bTOIqbVeMPG6%2B42Sp%2BRt3DAHXeFKES8%2Ffx33kfuQU7g%3D%3D; JTENANTSESSIONID_sapitcloud=gbmy1MFYbFETpHy4J2ps9KPBX6iNBYduoTj9q4ztwi4%3D; mdsoucrslenvcpoxerpvfurovbgp=EU7ooqy%2FMP1nCCdmoVqM51yP5RpuwjJxkNwXrgjxYZLn4jqv6rMCE9cpimpPs8X6ztwwzxgkusbgwJNHersYkGEoN7UXFaM%2BpM3nhtjyRuWpQWEd0Yg7pdcElEdYFGJAbtoT1wIhwb30sSO8%2Fn3CuU8afKLNZ15NzX3ZXbXpx%2BqVp2SEqZSDsnW%2FO80Ujp3LEjldjY3YMrVt6nsDBWYQkjMMz3KEQ5ETFs2FRn7QSxUYCrKCnYzMUxHxUz3%2BoSYxudPDoFSA1wEj7ln4YOm7xoXYM9jtscpSKKv4JFWNv9nxgUOVWLqe%2FKRhK26vMvg2t5FaAd1vRipsmx2qJsk41FaVobPGbZZKxPyW7ximN%2B0L2qHDAZSTLkY919xgnuf5sXIWVrMY5qEhepmrX8Wa%2FA%3D%3D; JTENANTSESSIONID_yrfr8dh9z4=lDCtiXfEmibLvAo2cIVGw5p0Cv4wfq3Ltyyh3s7OqRA%3D; __VCAP_ID__=8361d70b-1dfc-48d0-744f-3c3695adcf06; Current-User=%7B%22userId%22%3A%22b086478d-6c6c-45bf-b99c-48c818d62d81%22%7D; JSESSIONID=NWJjZmJlMTYtMTliZC00MzdkLTg2ZGEtOWMwYzRlNzM1MDk0; X-Uaa-Csrf=-pe59WPx-3-6woMIuAsPJx",
    "Referer": "https://accounts.sap.com/",
    "Referrer-Policy": "origin"
  },
  "body": null,
  "method": "GET"
});

console.log(response);
