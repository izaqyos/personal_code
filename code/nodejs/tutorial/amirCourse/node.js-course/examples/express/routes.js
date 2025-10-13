var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.use(bodyParser.json({limit: "10mb"})); // json payload
app.use(bodyParser.urlencoded({extended: true})); // form data, w/o multipart

app.get('/users', function (req, res) {
    res.send('Got a GET request');
});

app.post('/users', function (req, res) {
    console.log("req.body:", req.body);
    res.send('Got a POST request');
});

// PUT http://localhost:3000/users/120321/posts/a10b234122?lang=he
// --> req.params: { "userId": "120321", "postId": "a10b234122" }
// --> req.query: { "lang": "he" }
app.put('/users/:userId/posts/:postId', function (req, res) {
    res.json({'req.params': req.params, 'req.query': req.query});
});

app.delete('/users/:id', function (req, res, next) {
    // route filter which validates the given id
    if (req.params.id.length > 4) {
        next();
    } else {
        next("Error: not valid id");
    }
}, function (req, res) {
    res.json({result:'Got a DELETE request at /users/:id with id=' + req.params.id});
});

app.use("/admin", require("./router"));

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});