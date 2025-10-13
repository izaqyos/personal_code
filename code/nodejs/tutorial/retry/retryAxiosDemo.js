
const rax = require('retry-axios');
const axios = require('axios');


getTestLocal = async function(){
        console.log("Example of using global axios instance with default retry-axios config");
        let res;
        try{
            const interceptorId = rax.attach();
            res = await axios.get('https://test.local');
        }
        catch (err){
                console.log(err);
        }
}

getTestLocalMyAxios = async function(){
        console.log("Example of using custom axios instance with default retry-axios config");
        const myAxios = axios.create();
        myAxios.defaults.raxConfig = {
                instance: myAxios,
                retryDelay: 60000
        };
        let res;
        try{
            const interceptorId = rax.attach(myAxios);
            res = await myAxios.get('https://test.local');
        }
        catch (err){
                console.log(err);
        }
}

getAxiosConfig = async function (){
const interceptorId = rax.attach();
const res = await axios({
  url: 'https://test.local',
  raxConfig: {
    // Retry 3 times on requests that return a response (500, etc) before giving up.  Defaults to 3.
    retry: 3,
 
    // Retry twice on errors that don't return a response (ENOTFOUND, ETIMEDOUT, etc).
    noResponseRetries: 2,
 
    // Milliseconds to delay at first.  Defaults to 100.
    retryDelay: 10000,
 
    // HTTP methods to automatically retry.  Defaults to:
    // ['GET', 'HEAD', 'OPTIONS', 'DELETE', 'PUT']
    httpMethodsToRetry: ['GET', 'HEAD', 'OPTIONS', 'DELETE', 'PUT'],
 
    // The response status codes to retry.  Supports a double
    // array with a list of ranges.  Defaults to:
    // [[100, 199], [429, 429], [500, 599]]
    statusCodesToRetry: [[100, 199], [429, 429], [500, 599]],
 
    // If you are using a non static instance of Axios you need
    // to pass that instance here (const ax = axios.create())
    //instance: ax,
 
    // You can detect when a retry is happening, and figure out how many
    // retry attempts have been made
    onRetryAttempt: (err) => {
            const cfg = rax.getConfig(err);
            let hrend = process.hrtime(hrstart);
            //console.log(`Retry attempt #${cfg.currentRetryAttempt}`);
            console.log(`Retry attempt #${cfg.currentRetryAttempt}`);
            console.log('elapsed time since start of request: %ds %dms.', hrend[0], hrend[1]/1000000);
    }
  }
}).then(function(err){
        console.log('caught err ', err);
});;
}
getTestCostumRAX = async function(){
        console.log("Example of using custom axios instance with custom retry-axios config");
        const myAxios = axios.create();
        myAxios.defaults.raxConfig = {
                //retry on responses like 5xx
                retry: 3,
                //retry on ENOTFOUND, ETIMEDOUT etc
                noResponseRetries: 10,
                // Milliseconds to delay at first.  Defaults to 100.
                retryDelay: 60000,

                // HTTP methods to automatically retry.  Defaults to:
                // ['GET', 'HEAD', 'OPTIONS', 'DELETE', 'PUT']
                //httpMethodsToRetry: ['GET', 'HEAD', 'OPTIONS', 'DELETE', 'PUT'],

                // The response status codes to retry.  Supports a double
                // array with a list of ranges.  Defaults to:
                // [[100, 199], [429, 429], [500, 599]]
                statusCodesToRetry: [[100, 199], [429, 429], [500, 599]],

                // If you are using a non static instance of Axios you need
                // to pass that instance here (const ax = axios.create())
                instance: myAxios,
                // You can detect when a retry is happening, and figure out how many
                // retry attempts have been made
                onRetryAttempt: (err) => {
                        //const cfg = rax.getConfig(err);
                        let hrend = process.hrtime(hrstart);
                        //console.log(`Retry attempt #${cfg.currentRetryAttempt}`);
                        console.log('elapsed time since start of request: %ds %dms.', hrend[0], hrend[1]/1000000);
                }
        };
        let res;
        try{
            const interceptorId = rax.attach(myAxios);
            res = await myAxios.get('https://test.local');
        }
        catch (err){
                console.log('caught error: ', err);
        }
}


//const repetitions = 2;
//for( i=0; i<repetitions; i++){
//        console.log("firing axios GET. iteration ",i);
//        //getTestLocal();
//        //getTestLocalMyAxios(); 
//        getTestCostumRAX();
//        }

console.log('measure retry times');
let hrstart = process.hrtime();
//getTestCostumRAX();
//getAxiosConfig(); 
getTestLocalMyAxios() ;
let hrend = process.hrtime(hrstart);
console.log('supposed supposed retry time: %ds %dms. meaningless since it comes from main thread', hrend[0], hrend[1]/1000000);
