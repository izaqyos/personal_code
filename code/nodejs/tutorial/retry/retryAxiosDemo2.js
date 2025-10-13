'use strict';

const
    axios = require('axios'),
    rax = require('retry-axios');

const
    retryAxiosInstance = axios.create(),
    defaultRetryConfig = {
        retry: 3,
        noResponseRetries: 3,
        retryDelay: 100,
        httpMethodsToRetry: ['GET', 'DELETE', 'PUT', 'POST'],
        instance: retryAxiosInstance,
        statusCodesToRetry: [[100, 199], [429, 429], [400, 404], [501, 599]],
        onRetryAttempt: (err) => {
            const retryConfig = rax.getConfig(err);
            console.log('retry:'+retryConfig.currentRetryAttempt);
        }
    };

rax.attach(retryAxiosInstance);
try{
let res = retryAxiosInstance.get('http://localhost/').catch( function(err) { console.log('promise catch retry error', err);});
}
catch (err){
        console.log('retry error ',err);
}


//class Retry {
//    getRetryAxios(loggerCtx, cfg, requestOptions = {}) {
//        //logger.logRequestMessage(loggerCtx, 'info', 'getRetryAxios - config %s', logger.printObject(cfg));
//
//        let retryConfig = Object.assign({}, defaultRetryConfig, cfg);
//        retryConfig.loggerCtx = loggerCtx; //store loggerCtx on retry, to be used later
//        requestOptions.raxConfig = retryConfig;
//
//        return retryAxiosInstance;
//    }
//}


