const http = require('http');

module.exports.start = (HttpServer, port = 3000, onListen) => {
    const server = http.createServer(serverFactory(HttpServer));
    server.listen(port, onListen || (() => console.log(`server is listening on port ${port}`)));
    return server;
};

module.exports.serverFactory = serverFactory;

module.exports.BaseHttpServer = class BaseHttpServer {
    async handle(req, res) {
        res.end();
    }
};

// private functions

function serverFactory(clazz) {
    const handler = new clazz();
    return (req, res) => handler.handle(req, res);
}