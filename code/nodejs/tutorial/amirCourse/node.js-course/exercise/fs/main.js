const utils = require("./utils");
const fs = require('fs');
const path = require('path');

const sPath = __dirname;//process.argv[2];
const pattern = utils.createPattern("*.js");

// TODO: complete
// 1. read desired directory
// 2. loop on files and look for matching files
// 3. print the content of file if match pattern

console.log("booo");

process.on("exit", function () {
    console.log("exit...");
});