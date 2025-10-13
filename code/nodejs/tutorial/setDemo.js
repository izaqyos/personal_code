console.log('Set() unique values...');

let arr2 = [1,3,2,2,6,4,4,1,1];
let set1 = new Set(arr2);
let arrUnique = Array.from(new Set(arr2))


console.log('Original array: ', arr2);
console.log('Set from array: ', set1);
console.log('Uniq array: ', arrUnique);

let arrofArr = [
    [1,3,5,7],
    [2,4,6,8],
    [1,3,6,9],
    [1,3,0,7],
    [1,2,5,7],
];

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flat
let flattenUniqArray = Array.from( new Set(arrofArr.flat()));
console.log('Original array of arrays: ', arrofArr);
console.log('flattend uniq array: ', flattenUniqArray);

// reduce and concat alternatives
var arr1 = [1, 2, [3, 4]];
arr1.flat();


//to flat single level array
arr1.reduce((acc, val) => acc.concat(val), []);// [1, 2, 3, 4]

//or
const flatSingle = arr => [].concat(...arr);
//to enable deep level flatten use recursion with reduce and concat
var arr1 = [1,2,3,[1,2,3,4, [2,3,4]]];

function flattenDeep(arr1) {
   return arr1.reduce((acc, val) => Array.isArray(val) ? acc.concat(flattenDeep(val)) : acc.concat(val), []);
}
flattenDeep(arr1);// [1, 2, 3, 1, 2, 3, 4, 2, 3, 4]
//non recursive flatten deep using a stack
var arr1 = [1,2,3,[1,2,3,4, [2,3,4]]];
function flatten(input) {
  const stack = [...input];
  const res = [];
  while (stack.length) {
    // pop value from stack
    const next = stack.pop();
    if (Array.isArray(next)) {
      // push back array items, won't modify the original input
      stack.push(...next);
    } else {
      res.push(next);
    }
  }
  //reverse to restore input order
  return res.reverse();
}
flatten(arr1);// [1, 2, 3, 1, 2, 3, 4, 2, 3, 4]
//recursive flatten deep
function flatten(array) {
  var flattend = [];
  !(function flat(array) {
    array.forEach(function(el) {
      if (Array.isArray(el)) flat(el);
      else flattend.push(el);
    });
  })(array);
  return flattend;
}
