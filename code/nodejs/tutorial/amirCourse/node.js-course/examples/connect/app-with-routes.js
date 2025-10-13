var connect = require('connect');
var morgan = require('morgan');
var bodyParser = require('body-parser');

var app = connect();

app.use(morgan('dev'));

app.use(bodyParser.json({limit: '10mb'}));

app.use('/route', require('./routes'));
// catch error in the given route
// throwing the error in order to propagate to next error handler
app.use('/route', function (err, req, res, next) {
    console.error("error in home router..");
    err.router = "route";
    next(err);
});

app.use(function (err, req, res, next) {
    console.error("Error:", err);
    res.statusCode = err.status || 500;
    res.end('Error:' + err.message || err);
});

app.listen(3000, function () {
    console.log("server is up!");
});
