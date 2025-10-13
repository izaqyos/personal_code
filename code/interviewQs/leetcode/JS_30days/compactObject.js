/**
 Given an object or array obj, return a compact object.

A compact object is the same as the original object, except with keys containing falsy values removed.
 This operation applies to the object and any nested objects. Arrays are considered objects where the indices are keys. 
 A value is considered falsy when Boolean(value) returns false.

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
 * 
 */

/**
 * 
 * @param {Object|Array} obj
 * @return {Object|Array}
 */
var compactObject = function(obj) {

    function compactDFSRecursion(obj, newObj) {
        if (Array.isArray(obj)) {
            //console.log("handling as array, using newObj", newObj);
            // handle as array
            for (const val of obj) {
                //console.log("handling val", val);
                if (Boolean(val)) {
                    //console.log("handle non falsy val", val);
                    if (Array.isArray(val) ) {
                        //console.log("val type is array");
                        const compact_val = compactDFSRecursion(val, []);
                        //console.log("Adding to array compact val of type array ", compact_val);
                        newObj.push(compact_val);
                    } else if (typeof val === 'object') {
                        //console.log("val type is object");
                        const compact_val = compactDFSRecursion(val, {});
                        //console.log("Adding to array compact val of type object ", compact_val);
                        newObj.push(compact_val);
                    } else {
                        //console.log("Adding to array val", val);
                        newObj.push(val);
                    }
                }
            }
        } else if (typeof obj === 'object') {
            //handle as object
            //console.log("handling as object");
            for (const key in obj) {
                //console.log("handling key", key);
                if (Boolean(obj[key])) {
                    //console.log("handle non falsy key", key, "value", obj[key]);
                    if (Array.isArray(obj[key])) {
                        newObj[key] = compactDFSRecursion(obj[key], []);

                    } else if (typeof obj[key] === 'object'){
                        newObj[key] = compactDFSRecursion(obj[key], {});
                    } else {
                        newObj[key] = obj[key];
                    }
                }
            }
        }
        else {
            //console.log("Type is not an array or object")
        }
        return newObj;
    };

    if  (Array.isArray(obj)) {
        //console.log("Type is array", obj);
        return compactDFSRecursion(obj, []);
    } else if (typeof obj === 'object') {
        //console.log("Type is object", obj);
        return compactDFSRecursion(obj, {});
    }
};