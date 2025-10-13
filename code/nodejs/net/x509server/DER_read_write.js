const fs = require('fs');

const derBinary = fs.readFileSync(__dirname + '/x509/server-ca-crt.der');
console.log('Read DER in binary format. lenght', derBinary.length);

fs.writeFileSync(__dirname + '/x509/server-ca-crt2.der', derBinary);
const der2Binary = fs.readFileSync(__dirname + '/x509/server-ca-crt2.der');

function compare_buffers(b1, b2) {
    if (b1.length !== b2.length) {
        return false;
    }

    for (let index = 0; index < b1.length; index++) {
        if (b1[index] !== b2[index]) {
            return false;
        } 
    }
    return true 
}

const same = compare_buffers(der2Binary, derBinary);
console.log(`It is ${same} that input and output DER files are equal`);



