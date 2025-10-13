const express = require('express');
const responseTime = require('response-time');
const asyncEcho = require('./async-echo');
const app = express();

// dummy filter, writes an header on the response
app.use((req, res, next) => {
    console.log("dummy filter...");
    res.setHeader("X-Dummy-Header", "val");
    next();
});
// filter that writes total time of the response on header
app.use(responseTime());

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.get('/async', async (req, res) => {
    const result = await asyncEcho('Hello World!');
    res.send(result);
});

app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});