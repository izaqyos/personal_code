const express = require('express');
const bodyParser = require('body-parser');
const adminRouter = require('./router');
const echoRouter = require('./echo-router');

const app = express();

app.use(bodyParser.json({limit: "10mb"})); // json payload

app.use('/admin', adminRouter);

app.use('/echo', echoRouter());

app.use((req, res) => {
    console.log("boo");
    res.json({hello: "world"});
});

app.listen(3000, () => {
    console.log("App is running...");
});