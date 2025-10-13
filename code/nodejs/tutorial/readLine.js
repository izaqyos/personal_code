const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})

readline.question(`What's your name?`, (name) => {
        readline.question(`What's your surname?`, (surname) => {
            console.log(`Hi ${name} ${surname} !`);
            readline.close();
        });
})
