/**
 * @param {Function} fn
 * @return {Function}
 */
function memoize(fn) {
    
    const cacheMap = new Map();
    return function(...args) {
        //console.log(...cacheMap);
        let key = args.join(',');
        if (cacheMap.has(key)) {
            //console.log("result already exist for", key);
            return cacheMap.get(key);
        } 
        //console.log("calling once",fn,args);
        let value = fn(...args);
        cacheMap.set(key, value);
        return value;
    }
}









/** 
 * let callCount = 0;
 * const memoizedFn = memoize(function (a, b) {
 *	 callCount += 1;
 *   return a + b;
 * })
 * memoizedFn(2, 3) // 5
 * memoizedFn(2, 3) // 5
 * console.log(callCount) // 1 
 */