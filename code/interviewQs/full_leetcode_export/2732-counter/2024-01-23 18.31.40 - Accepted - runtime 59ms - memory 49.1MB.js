/**
 * @param {number} n
 * @return {Function} counter
 */
var createCounter = function(n) {
    
    let _n = n;
    return function() {
        return n++;
    };
};

/** 
 * const counter = createCounter(10)
 * counter() // 10
 * counter() // 11
 * counter() // 12
 */