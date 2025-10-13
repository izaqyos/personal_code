process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0
const request = require('request')
var username = '<user>'
var password = '<password>'
var options = {
  url: 'https://host.example.com:44300/api/entities',
  auth: {
    user: username,
    password: password
  }
}

request(options, function (err, res, body) {
  if (err) {
    console.dir(err)
    return
  }
  console.dir('headers', res.headers)
  console.dir('status code', res.statusCode)
  console.dir(body)
})
