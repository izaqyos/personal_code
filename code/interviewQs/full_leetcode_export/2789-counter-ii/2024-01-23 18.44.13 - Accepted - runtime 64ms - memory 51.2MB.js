/**
 * @param {integer} init
 * @return { increment: Function, decrement: Function, reset: Function }
 */
var createCounter = function(init) {
    let _init = init;
    let _current = init;
    return {
        'increment' : () => {
           return ++_current; 
        },
        'decrement' : () => {
           return --_current; 
        },
        'reset' : () => {
            _current = _init;
           return _current; 
        },
    };
    
};

/**
 * const counter = createCounter(5)
 * counter.increment(); // 6
 * counter.reset(); // 5
 * counter.decrement(); // 4
 */