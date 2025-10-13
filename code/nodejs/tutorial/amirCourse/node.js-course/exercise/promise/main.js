var dir = process.argv[2] || "";
var p = process.argv[3] || "";

var Q = require('q');
var utils = require('./utils');
var pattern = utils.createPattern(p);

var start = new Date();
console.log("starting at:", start);

//// write your code ////

process.on('exit', function () {
    var end = new Date();
    console.log("finished !!!");
    console.log("time:", end);
    console.log("total ms:", end - start);
});
