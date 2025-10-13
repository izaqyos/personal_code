var _ = require('lodash');
var connectRoute = require('connect-route');

module.exports = connectRoute(function (router) {
    router.get('/home', function (req, res, next) {
        res.end('home');
    });

    router.get('/home/:id', function (req, res, next) {
        res.end('home with id:' + req.params.id);
    });

    router.post('/home/:id', function (req, res, next) {
        res.end('home with id:' + req.param.id
            + '\nand payload:'
            + _.attempt(JSON.stringify.bind(null, req.body)));
    });

});

