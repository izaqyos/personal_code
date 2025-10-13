
/*
Given an array of functions [f1, f2, f3, ..., fn], return a new function fn that is the function composition of the array of functions.

The function composition of [f(x), g(x), h(x)] is fn(x) = f(g(h(x))).

The function composition of an empty list of functions is the identity function f(x) = x.

You may assume each function in the array accepts one integer as input and returns one integer as output.
 */

const assert = require('assert');

var compose = function(functions) {
    
    return function(x) {
        res = x;
        if (functions) {
            for (let i = functions.length -1; i >= 0 ; i--) {
                res = functions[i](res);
            }
        } 
       return res; 
    }
};

const test1 = function(){
    const functions = [x => x + 1, x => x * x, x => 2 * x]
    const x = 4;
    const expected = 65;
    val = compose(functions)(x);
    assert.equal(val , expected, "not equal");
}

const test2 = function(){
    const functions = [x => 10 * x, x => 10 * x, x => 10 * x]
    const x = 1;
    const expected = 1000;
    val = compose(functions)(x);
    assert.equal(val , expected, "not equal");
}

const test3 = function(){
    const functions = []
    const x = 42;
    const expected = 42;
    val = compose(functions)(x);
    assert.equal(val , expected, "not equal");
}

let test = function() {
    test1();
    test2();
    test3();
};

test();
