const pem = require("pem");
const fs = require("fs");

const pfx = fs.readFileSync(__dirname + "/x509/client-crt.pfx");
pem.readPkcs12(pfx, { p12Password: "1234" }, (err, cert) => {
    if (err) {
        console.log(err);
    } else {
    console.log(cert);
    }
});
