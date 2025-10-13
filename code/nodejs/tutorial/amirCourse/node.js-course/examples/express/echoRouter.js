'use strict';

const express = require('express');

module.exports = () => {
    let router = express.Router();

    router.post('/', (req, res, next) => {
            res.send(req.body.arg);
    });

    router.get('/:arg', (req, res, next) => {
            res.send(req.params.arg);
    });

    return router;
};

module.exports._route = '/echo';

