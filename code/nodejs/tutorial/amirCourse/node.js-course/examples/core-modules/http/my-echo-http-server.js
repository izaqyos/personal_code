const {BaseHttpServer} = require('./my-http-lib');

module.exports = class MyEchoHttpServer extends BaseHttpServer {
    async handle(req, res) {
        return req.pipe(res);
    }
};