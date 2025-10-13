"use strict";
const express = require('express');
const app = express();
const CoinRouter = require('./routes/CoinRouter.js');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const path = require('path');

app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.set('view engine', 'ejs');

const port = 3030;
mongoose.connect('mongodb://localhost/expressdemo');

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.use('/coins', CoinRouter);

async function initServer() {
new Promise((resolve) => {
        app.listen(port, () => {
            console.log('express demo is listening on port %d', port);
            resolve();
        });
    });
}
initServer();

// app.listen(port, () => {
//     console.log('Welcome to express demo');
// });
