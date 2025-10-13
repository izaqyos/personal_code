const axios = require('axios');
const request = require('request');
// const redis = require('./redis-client');

const baseUrl = "https://randomuser.me";

const proxy = async ({ path, method = 'get', body}) => {
    // TODO:
    //  1. do an api call using axios
    //  2. use redis to build a cache on top the API call
    return { };
};

const proxyAsset = (path, res) => {
    const response = request.get(`${baseUrl}/${path}`);
    return response.pipe(res);
};

module.exports = {
    proxy,
    proxyAsset
};