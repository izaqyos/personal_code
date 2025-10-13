var fs = require('fs'),
    Q = require('q'),
    Minimatch = require("minimatch").Minimatch;

module.exports = {
    createPattern: function (pattern) {
        return new Minimatch(pattern);
    },
    getDirContent: function (path) {
        // TODO: implement.. hint: fs.readdir
        // should return a promise
    },
    isDir: function isDir(path) {
        // TODO: implement.. hint: fs.lstat
        // should return a promise
    }
};