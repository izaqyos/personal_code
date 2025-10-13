var express = require('express');
var router = express.Router();
var watchers = [];

router.use(function (req, res, next) {
    console.log("watchers router...");
    res.setHeader("X-Dummy-Header", "val");
    next();
});

router.get('/', function (req, res) {
    res.json(watchers);
});

module.exports = router;
