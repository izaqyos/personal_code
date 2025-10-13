var path = require('path');
var connect = require('connect');

var morgan = require('morgan');
var bodyParser = require('body-parser');
var compression = require('compression');
var serveStatic = require('serve-static');

var app = connect();

// gzip / deflate
app.use(compression());

// logging
app.use(morgan('dev'));

// parse json payload
app.use(bodyParser.json({limit: '10mb'}));
// print payload to log...
app.use(function (req, res, next) {
    console.log("req payload:", req.body);
    next();
});

var connectJson = require('./connect-json');
app.use(connectJson());

var connectXML = require('./connect-xml');
app.use(connectXML());

// static resources
app.use(serveStatic(path.join(__dirname, 'public')));

app.use('/hello', function (req, res, next) {
    res.json({hello: "world"});
});

app.use('/helloxml', function (req, res, next) {
    res.xml({hello: "world"});
});

// Error handler
app.use(function (err, req, res, next) {
    res.statusCode = err.status || 500;
    res.end('Error:' + err.message || err);
});

app.listen(3000, function () {
    console.log('server is up!');
});