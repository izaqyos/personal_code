const {server, client} = require("../lib");

class MyHttpServer extends server.BaseHttpServer {
    handle(req, res) {
        // host: localhost, port: 8001, path: "/posts"
        client({
            host: "localhost",
            port: 8001,
            path: "/posts",
            isStream: true
        }, (err, stream) => {
            stream.pipe(res);
        });
    }
}

server.start(MyHttpServer, 3000);