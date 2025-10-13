var crypto = require('crypto');

let dosomething = () => {
    for (var i = 0, len = 1000000; i < len; i++) {
    crypto.createCipher('aes-128-cbc', 'mypassword');
    //var mykey = crypto.createCipher('aes-128-cbc', 'mypassword');
//var mystr = mykey.update('abc', 'utf8', 'hex')
//mystr += mykey.final('hex');
        
    }

}

somethingHeavy = function () {
    // goes through libuv and does heavy calcs
    // takes 1 SECOND
    dosomething()
    console.log('calc done')
}

const request = require('request')

googleRequest = function () {
    // fires http request to google
    request('https://www.google.com',  (err, res, body) => {
        if (err) { console.log(err);}
        console.log('back from google')
    })
}

const fs = require('fs');

googleRequest()
fs.readFile('libuvquestion.js', 'utf-8', () => {
    console.log('read done')
})

somethingHeavy()
somethingHeavy()
somethingHeavy()
somethingHeavy()

