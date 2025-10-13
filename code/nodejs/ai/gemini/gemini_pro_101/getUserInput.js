const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

async function getPrompt() {
let lname;
readline.question('What is your name? ', (name) => {
    lname = name;
    // console.log(`Hello CB, ${lname}!`);
    readline.close(); // Close the interface after getting input

});

return lname;
}

prompt = await getPrompt();
console.log(`Hello, ${prompt}!`);