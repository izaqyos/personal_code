var passport = require('passport');
var Strategy = require('passport-local').Strategy;
var localStrategyHandler = require('./local-strategy-handler');
var sessionSerializer = require('./session-serializer');

passport.use(new Strategy(localStrategyHandler));

sessionSerializer(passport);

module.exports = passport;