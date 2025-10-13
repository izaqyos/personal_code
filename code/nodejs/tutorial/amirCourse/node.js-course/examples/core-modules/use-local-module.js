const localModule = require('./local-module');

console.log(localModule.getVar()); // > undefined
localModule.setVar("Hello local module!");
console.log(localModule.getVar()); // > Hello local module!
