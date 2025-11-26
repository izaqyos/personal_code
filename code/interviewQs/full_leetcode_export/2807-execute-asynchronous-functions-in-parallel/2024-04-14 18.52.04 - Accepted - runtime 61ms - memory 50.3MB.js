/**
 * @param {Array<Function>} functions
 * @return {Promise<any>}
 */
var promiseAll = function(functions) {
    return new Promise(async (res, rej) => {
        const retVals = [];
        let unfulfilledPromises = functions.length;
        functions.forEach((func, index) => {
            func()
            .then((val) => {
                retVals[index] = val;
                unfulfilledPromises--;
                if (unfulfilledPromises === 0) {
                    res(retVals);
                }
            })
            .catch((err) => {
                rej(err);
            })
        });
    });
}
/**
 * const promise = promiseAll([() => new Promise(res => res(42))])
 * promise.then(console.log); // [42]
 */