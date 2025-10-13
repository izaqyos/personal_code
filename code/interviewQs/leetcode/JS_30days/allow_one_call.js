/*
Given a function fn, return a new function that is identical to the original function except that it ensures fn is called at most once.

The first time the returned function is called, it should return the same result as fn.
Every subsequent time it is called, it should return undefined.
*/

var once = function(fn) {
    let called = 0;
    return function(...args){
        console.log(`called = ${called}`);
        if (called > 0) {
            return undefined;
        }
        called++;
        return fn(...args);
    }
};

const test1 = function() {

    const fn = (a,b,c) => (a + b + c);
    calls = [[1,2,3],[2,3,6]];
    let res;

    const oncefunc  = once(fn);
    for (const elem of calls) {
        res = oncefunc(elem);
        console.log(`calling once with args ${elem}, result is ${res}`);
    }
}
let test = function() {
    test1();
//    test2();
//    test3();
};

test();

