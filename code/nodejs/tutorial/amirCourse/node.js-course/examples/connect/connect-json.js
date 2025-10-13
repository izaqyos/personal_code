module.exports = function (opts) {
    return function (req, res, next) {
        res.json = function (obj) {
            this.setHeader("Content-Type", "application/json");
            this.end(JSON.stringify(obj));
        };
        next();
    };
};
