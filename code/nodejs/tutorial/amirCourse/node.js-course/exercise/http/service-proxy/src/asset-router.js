const express = require('express');
const serviceClient = require('./service-client');

module.exports = () => {
    const router = express.Router();

    router._baseRoute = '/asset';

    // currently, the path gets passed using query parameter (/asset/?path=<path>)
    // TODO: read path from the URL itself (/asset/<path>)

    router.get('/*', async (req, res) => {
        const { path } = req.query;
        await serviceClient.proxyAsset(path, res);
    });

    router.use((err, req, res, next) => {
        console.error('error during asset call:', err);
        throw err;
    });

    return router;
};