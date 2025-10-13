const express = require('express');
const serviceClient = require('./service-client');

module.exports = () => {
    const router = express.Router();

    router._baseRoute = '/api';

    // currently, the path gets passed using query parameter (/api/?path=<path>)
    // TODO: read path from the URL itself (/api/<path>)

    router.post('/*', async (req, res) => {
        const path = req.query.path;
        const result = await serviceClient.proxy(path, req.body);
        res.json(result);
    });

    router.get('/*', async (req, res) => {
        const { path } = req.query;
        const result = await serviceClient.proxy({ path });
        res.json(result);
    });

    router.use((err, req, res, next) => {
        console.error('error during api call:', err);
        throw err;
    });

    return router;
};