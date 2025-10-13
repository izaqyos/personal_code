const { BaseHttpServer } = require('./my-http-lib');

const urlRegex = /^\/dummy/;
const allowedMethods = ['POST', 'GET'];

module.exports = class MyDummyHttpServer extends BaseHttpServer {
    async handle(req, res) {
        const filtered = await this.filter(req, res);
        if (filtered.valid) {
            res.writeHead(200);
            res.end("Hello Node js !!!");
            return true;
        }
        res.writeHead(filtered.statusCode || 404);
        return super.handle(req, res);
    }

    filter(req, res) {
        const {url, method} = req;
        const validURL = urlRegex.test(url);
        const validMethod = allowedMethods.indexOf(method) >= 0;
        return {
            valid: validURL && validMethod,
            statusCode: !validURL ? 404 : 0
        };
    }
}