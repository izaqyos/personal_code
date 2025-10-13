var express = require('express');
var app = express();

require('./expressPlugins')(app);

require('./routes')(app);

require('./errors')(app);

module.exports = app;
