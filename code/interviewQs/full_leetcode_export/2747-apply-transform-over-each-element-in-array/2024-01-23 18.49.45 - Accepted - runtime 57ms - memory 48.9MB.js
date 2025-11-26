/**
 * @param {number[]} arr
 * @param {Function} fn
 * @return {number[]}
 */
var map = function(arr, fn) {
    let new_arr = [...arr];
    for (let i=0; i<new_arr.length; i++) {
        new_arr[i] = fn(new_arr[i], i);
    }
    return new_arr;
};