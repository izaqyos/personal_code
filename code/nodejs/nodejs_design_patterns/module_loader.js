const fs = require('fs');
const path = require('path');

function loadModule(filename, module, require) {
    console.log(`loading source code of ${filename}`);
    var wrappedSrc =
        '(function(module, exports, require) {' +
        fs.readFileSync(filename, 'utf8') +
        '})(module, module.exports, require);';
    eval(wrappedSrc);
}

var my_require = function(moduleName) {
    console.log('Require invoked for module: ' + moduleName);
    // var id = require.resolve(moduleName);
    let id =  require.resolve(moduleName);
    if(my_require.cache[id]) {
        return my_require.cache[id].exports;
    }
    //module metadata
    var module = {
        exports: {},
        id: id };   //Update the cache
    my_require.cache[id] = module;
    //load the module
    loadModule(id, module, my_require);
    //return exported variables
    return module.exports;
};
my_require.cache = {};
my_require.resolve = function(moduleName) {
    /* resolve a full module id from the moduleName */
    return path.basename(moduleName);
}

let foo = my_require('./foo_module.js');
foo.run();
console.log(JSON.stringify(foo, null, 4));
