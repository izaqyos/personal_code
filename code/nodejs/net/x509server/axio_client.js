const fs = require('fs');
const https = require('https');
const axios = require('axios');

// use for my demo x509 server
// const port = '4433';
// const urlpath= ''

// use for my mock provider  x509 server
const port = '3000';
let urlpath= '/devutils/static/uyz.json'

const httpsAgent = new https.Agent({
    cert: fs.readFileSync(__dirname + '/x509/client-crt.pem'),
    key: fs.readFileSync(__dirname + '/x509/client-key.pem'),
    rejectUnauthorized: false, // required to prevent UNABLE_TO_VERIFY_LEAF_SIGNATURE error
    passphrase: '1234',
    // pfx: fs.readFileSync(__dirname + '/x509/client-crt.pfx'),
    // ca: [fs.readFileSync(__dirname + '/x509/server-ca-crt.pem')],
    // maxVersion: 'TLSv1.3',
    // minVersion: 'TLSv1.3',
     ca: fs.readFileSync('x509/server-ca-crt.pem'),
});

urlpath='https://localhost'+':'+port+urlpath;
console.log('url: ', urlpath);
axios.get(urlpath, { httpsAgent }).then((response) => {
    console.log(response.data);
}, (error) => {
    console.log(error.code);
});

