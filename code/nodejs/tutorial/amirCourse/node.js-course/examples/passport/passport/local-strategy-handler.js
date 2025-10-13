var db = require('../db');

module.exports = function(username, password, cb) {
    db.users.findByUsername(username, function(err, user) {
        if (err) { return cb(err); }
        if (!user) { return cb(null, false, "user does not exist"); }
        if (user.password != password) { return cb(null, false, "invalid password"); }
        return cb(null, user);
    });
};