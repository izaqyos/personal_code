var fs = require('fs')
var jwt = require('jsonwebtoken');
// sign with RSA SHA256
var cert = fs.readFileSync('private.key');

jwt.sign({ foo: 'bar' }, cert, { algorithm: 'RS256' }, function(err, token) {
  console.log(token);
});
