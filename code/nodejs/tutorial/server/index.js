var  express = require('express');

var app = express();

var users = ['boris', 'dean', 'asaf', 'yosi'];

app.get('/api/users', function(req, res){
        console.log("res=%o", res.json(users));
        res.json(users);
});

module.exports = app;
