//var dependency = my_require('./error_propogation.js');

//private API
function log(){
    console.log('example module');
}

//public API 
module.exports.run = function() {
    log();
}


