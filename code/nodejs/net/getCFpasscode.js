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
    "cookie": "<redacted>",
    "Referer": "https://accounts.sap.com/",
    "Referrer-Policy": "origin"
  },
  "body": null,
  "method": "GET"
});

console.log(response);
