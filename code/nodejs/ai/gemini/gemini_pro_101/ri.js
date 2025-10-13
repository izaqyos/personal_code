const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Please enter your name: ', (name) => {
  console.log(`Hello, ${name}!`);
  
  // Do something with the user input
  // For example, you can store it in a variable
  const userInput = name;

  // Once you've finished using the readline interface, close it
  rl.close();
});
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Please enter your name: ', (name) => {
  console.log(`Hello, ${name}!`);
  
  // Do something with the user input
  // For example, you can store it in a variable
  const userInput = name;

  // Once you've finished using the readline interface, close it
  rl.close();
});

