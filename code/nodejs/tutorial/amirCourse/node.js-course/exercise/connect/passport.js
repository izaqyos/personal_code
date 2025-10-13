var passport = require('passport'),
    LocalStrategy = require('passport-local').Strategy;

// TODO define your local strategy
// find the desired user
//  not found -> done(null, false, { message: 'Incorrect username.' });
//  wrong password -> done(null, false, { message: 'Incorrect password.' });
//  valid -> return done(null, user);

// TODO de/serialize user

module.exports = passport;