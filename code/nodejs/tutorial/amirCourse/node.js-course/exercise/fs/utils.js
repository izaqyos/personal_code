const Minimatch = require("minimatch").Minimatch;

module.exports = {
    createPattern: function (pattern) {
        return new Minimatch(pattern);
    }
};