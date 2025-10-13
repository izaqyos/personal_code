'use strict';

const request = require('request');
const fs = require('fs');

var options = {
    // rejectUnauthorized: false, // required to prevent UNABLE_TO_VERIFY_LEAF_SIGNATURE error, if the server CA is ok it is not required
    method: "GET",
    url: 'https://localhost:4433',
    headers: {
        "content-type": "application/json",
    },
    agentOptions: {
        // either client cert+pvk or pfx...
        cert: fs.readFileSync(__dirname + '/x509/client-crt.pem'),
        key: fs.readFileSync(__dirname + '/x509/client-key.pem'),
        // pfx: fs.readFileSync(__dirname + '/x509/client-crt.pfx'),

        passphrase: '1234',
        ca: [fs.readFileSync(__dirname + '/x509/server-ca-crt.pem')],
    }
};

request.get(options, (error, response, body) => {
    // console.log(error);
    // console.log(response);
    console.log(body);
});
