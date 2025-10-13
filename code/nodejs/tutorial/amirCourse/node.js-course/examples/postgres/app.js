var express = require('express');
var db = require("./db");
var app = express();
var PORT = process.env.NODE_PORT || 3000;

app.get('/', function (req, res, next) {
    db.getConnection()
        .then(function (connection) {
            connection.client.query('SELECT * FROM Student', function(err, result) {
                connection.done(); // closing the connection;
                if(err){
                    return next(err);
                }
                res.status(200).send(result.rows);
            });
        });
});

app.listen(PORT, function () {
    console.log('Server is running.. on Port ' + PORT);
});