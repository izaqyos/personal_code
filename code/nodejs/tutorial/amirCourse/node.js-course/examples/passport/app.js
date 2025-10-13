var connect = require('connect');
var db = require('./db');

var morgan = require('morgan');
var bodyParser = require('body-parser');
var session = require('express-session');
var passport = require('./passport');

var app = connect();

app.use(bodyParser.json({limit: '10mb'}));
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({ secret: 'keyboard cat', resave: false, saveUninitialized: false }));

// Initialize Passport and restore authentication state, if any, from the
// session.
app.use(passport.initialize());
app.use(passport.session());

app.use('/login', function(req, res, next) {
    if (req.method === "POST") {
        return passport.authenticate('local')(req, res, next);
    }
    res.end();
});

app.use('/private', function (req, res, next) {
    if (req.user) {
        return next();
    }
    next({message: 'Not authenticated', status: 401});
});
app.use('/private', require('./private-route'));

// Error handler
app.use(function (err, req, res, next) {
    res.statusCode = err.status || 500;
    res.end('Error:' + err.message || err);
});

app.listen(3000, function () {
    console.log('server is up!');
});