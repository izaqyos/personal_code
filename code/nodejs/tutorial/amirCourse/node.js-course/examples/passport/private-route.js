var connectRoute = require('connect-route');

module.exports = connectRoute(function (router) {
    router.get('/', function (req, res, next) {
        res.end('private...');
    });

    router.get('/private/:id', function (req, res, next) {
        res.end('private with id:' + req.params.id);
    });
});