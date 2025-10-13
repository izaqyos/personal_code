var path = require('path');
var connect = require('connect');
var morgan = require('morgan');

var app = connect();

// logging
app.use(morgan('dev'));

app.use('/error', function (req, res, next) {
    // throwing error by passing first param to next()
    next({message: 'my error', status: 407});
});

app.use('/exception', function (req, res, next) {
    // unexpected error
    myEmptyVar.dummy(); // exception: myEmptyVar is not defined
});

// Error handler
app.use(function (err, req, res, next) {
    res.statusCode = err.status || 500;
    res.end('Error:' + err.message || err);
});

app.listen(3000, function () {
    console.log('server is up!');
});