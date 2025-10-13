var connect = require("connect");
var app = connect();

// request for this path will be responded with error
app.use('/favicon.ico', function (req, res, next) {
    console.error("Missing favicon");
    next("Oops, youre not allowed..");
});

app.use(function (req, res, next) {
    console.log("first middleware");
    next();
});

app.use(function (req, res, next) {
    console.log("second middleware");
    next();
});
// will get to this filter only for url: <host>/third
app.use('/special', function (req, res, next) {
    console.log("special middleware");
    next();
});

app.use(function (req, res, next) {
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello Connect');
});

app.listen(3000, function () {
    console.log("server is up!");
});