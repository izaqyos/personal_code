const express = require('express');
const fs = require('fs');
const https = require('https');
const app = express();
const options = {
    key: fs.readFileSync('x509/server-key.pem'),
    cert: fs.readFileSync('x509/server-crt.pem'),
    ca: fs.readFileSync('x509/client-ca-crt.pem'),
    // ca: fs.readFileSync('x509/client-ca-crt.pem'),
    requestCert: true,
    rejectUnauthorized: true,
};
app.use(function (req, res, next) {
    console.log('ATN/ATZ middleware activated');
    if (! req.client.authorized) {
        console.log('ATZ failed');
        return res.status(401).send('User is not authorized');
    }
    console.log('checking peer certificate');
    const cert = req.socket.getPeerCertificate();
    if (cert.subject) {
        console.log('cert subject', cert.subject.CN);
        //console.log(JSON.stringify(cert, null, 4));
    }
    res.writeHead(200);
    res.end("hello world\n");
    next();
});
var listener = https.createServer(options, app).listen(4433, function () {
    console.log('Express HTTPS server listening on port ' + listener.address().port);
});
