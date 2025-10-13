const myHttp = require('./my-http-lib');
const MyEchoHttpServer = require('./my-echo-http-server');
const MyDummyHttpServer = require('./my-dummy-http-server');

myHttp.start(MyEchoHttpServer, 8001);

myHttp.start(MyDummyHttpServer, 8002);

