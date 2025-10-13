const express = require('express');
const debug = require('morgan');
const bodyParser = require('body-parser');
const compression = require('compression');

const app = express();

// middlewares
app.use(compression());
app.use(debug('dev'));
app.use(bodyParser.json({limit: "50mb"}));

// end-points
// 1. '/api' - for api calls (application/json)
const apiRouter = require('./api-router')();
app.use(apiRouter._baseRoute, apiRouter);
// 2. '/asset' - for file requests
const assetRouter = require('./asset-router')();
app.use(assetRouter._baseRoute, assetRouter);

app.use((err, req, res, next) => {
    res.statusCode = err.status || 500;
    res.send('Error:' + err.message || err);
});

module.exports = app;