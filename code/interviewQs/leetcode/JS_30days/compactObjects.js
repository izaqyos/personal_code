/*
Given an object or array obj, return a compact object.

A compact object is the same as the original object, except with keys containing falsy values removed. This operation applies to the object and any nested objects. Arrays are considered objects where the indices are keys. A value is considered falsy when Boolean(value) returns false.

You may assume the obj is the output of JSON.parse. In other words, it is valid JSON.

 

Example 1:

Input: obj = [null, 0, false, 1]
Output: [1]
Explanation: All falsy values have been removed from the array.
Example 2:

Input: obj = {"a": null, "b": [false, 1]}
Output: {"b": [1]}
Explanation: obj["a"] and obj["b"][0] had falsy values and were removed.
Example 3:

Input: obj = [null, 0, 5, [0], [false, 16]]
Output: [5, [], [16]]
Explanation: obj[0], obj[1], obj[3][0], and obj[4][0] were falsy and removed.
 

Constraints:

obj is a valid JSON object
2 <= JSON.stringify(obj).length <= 106
 
 */


// I'll solve recursion, DFS and BFS

/**
 * @param {Object|Array} obj
 * @return {Object|Array}
 */
const compactObjectRecursion = function (obj, resultObj = {}) {
    // stop cond. if obj process all k,v in obj and add to resultObj and add non falsy values to resultObj 
    if (typeof obj === 'object' && !Array.isArray(obj)) {

    }  
    // if it is array process all array and add non falsy values 
    else if  Array.isArray(obj)  {

    }
}


 return compactObjectRecursion(obj[0]
var compactObject = function(obj) {
    const retObj = {   };
 return compactObjectRecursion(obj, retObj);
 //return compactObjectDFS(obj);
// return compactObjectBFS(obj);
   
};