let xml2js = require('xml2js');
let builder = new xml2js.Builder();

module.exports = function (opts) {
    return function (req, res, next) {
        res.xml = function (obj) {
            this.setHeader("Content-Type", "application/xml");
            this.end(builder.buildObject(obj));
        };
        next();
    };
};
