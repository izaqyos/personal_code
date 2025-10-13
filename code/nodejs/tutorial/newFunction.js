const readline = require('readline');

const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
});

console.log('creating functions dynamically demo');

rl.question(`plz enter valid js code for function body `, (code) => {
        console.log(`you have entered code  ${code}`);
        rl.close();
});
