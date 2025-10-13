
const _ = require('lodash');

let arr1 = [ 1,2, [1,2]];
let arr2 = [ 1,3, 4];
let arr3 = _.union(arr1,arr2);
console.log('demo union of array ', arr1,' and array ', arr2, 'union: ', arr3);

let arrays = [ arr1, arr2, arr3];
let arr4 = _.unionWith(...arrays, (a,b) => {return a===b;});
console.log('demo union of array of arrays ', arrays, 'lodash union: ', arr4);
let arr5 = Array.from(new Set(...arrays));
let set1 = new Set(...arrays);
console.log('demo union of array of arrays ', arrays, 'Set from arrays: ', set1, ' ES6 union: ', arr5);
