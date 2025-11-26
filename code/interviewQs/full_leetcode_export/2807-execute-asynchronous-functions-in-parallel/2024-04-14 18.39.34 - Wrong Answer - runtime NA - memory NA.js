/**
 * @param {Array<Function>} functions
 * @return {Promise<any>}
 */
var promiseAll = function(functions) {
      
    return async function (functions) {
        let retVals = [];
        try {
            for (const func of functions) {
                console.log(`dispatching ${func}`);
                let res = func();
                console.log(`adding result ${res} to returned results array`);
                retVals.push(res);
            }
        } catch (e) {
            console.log(`caught error ${e}`);
            throw e;
            /* handle error */
        }
    }
 
};

/**
 * const promise = promiseAll([() => new Promise(res => res(42))])
 * promise.then(console.log); // [42]
 */