process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0
const request = require('request')
var username = 'COHENADA'
var password = 'T7zRoU7J'
var options = {
  url: 'https://ldai1uyt.wdf.sap.corp:44300/sap/bc/ui2/poc_cdm3/entities?sap-client=100',
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
