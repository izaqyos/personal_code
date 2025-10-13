/*
Given a multi-dimensional array arr and a depth n, return a flattened version of that array.

A multi-dimensional array is a recursive data structure that contains integers or other multi-dimensional arrays.

A flattened array is a version of that array with some or all of the sub-arrays removed and replaced with the actual elements in that sub-array. This flattening operation should only be done if the current depth of nesting is less than n. The depth of the elements in the first array are considered to be 0.

Please solve it without the built-in Array.flat method.

 

Example 1:

Input
arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 0
Output
[1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]

Explanation
Passing a depth of n=0 will always result in the original array. This is because the smallest possible depth of a subarray (0) is not less than n=0. Thus, no subarray should be flattened. 
Example 2:

Input
arr = [1, 2, 3, [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 1
Output
[1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11], 12, 13, 14, 15]

Explanation
The subarrays starting with 4, 7, and 13 are all flattened. This is because their depth of 0 is less than 1. However [9, 10, 11] remains unflattened because its depth is 1.
Example 3:

Input
arr = [[1, 2, 3], [4, 5, 6], [7, 8, [9, 10, 11], 12], [13, 14, 15]]
n = 2
Output
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

Explanation
The maximum depth of any subarray is 1. Thus, all of them are flattened.
 

Constraints:

0 <= count of numbers in arr <= 105
0 <= count of subarrays in arr <= 105
maxDepth <= 1000
-1000 <= each number <= 1000
0 <= n <= 1000
*/

/**
 * @param {Array} arr
 * @param {number} depth
 * @return {Array}
 */
var flat = function (arr, n) {
  // First, iterative BFS solution

  if (n === 0) {
    return arr;
  }

  let depth = n;

  while (depth > 0) {
    const ret = [];
    // peel one level
    for (let i = 0; i < arr.length; i++) {
      if (typeof arr[i] === "number") {
        ret.push(arr[i]);
      } else {
        ret.push(...arr[i]);
      }
    }
    arr = ret;
    depth--;
  }

  return arr;
};

/*
asked gemini to comment on my solution.

got:
Absolutely! Let's analyze your iterative BFS solution and explore alternative recursive DFS and BFS approaches.

**Your Iterative BFS Solution**

Your solution is clever and efficient! Here's a breakdown:

* **Core Idea:**  The "peeling" approach in the `while` loop is excellent. You process the array level by level, flattening one depth at a time until the desired depth `n` is reached.
* **Type Checking:** The `typeof arr[i] === "number"` check is essential to distinguish between numbers and nested arrays.
* **Spread Operator:** Using the spread operator (`...arr[i]`) neatly handles the flattening of nested arrays.
* **Correctness:**  The code correctly handles the edge case of `n = 0`, returning the original array.

**Possible Optimizations:**

* **Early Termination:** You could add an optimization to check if the array is already flat (no nested arrays). If so, you can immediately return the array, saving unnecessary iterations.

**Recursive DFS Solution**

```javascript
function flat(arr, n) {
    const result = [];
    for (const item of arr) {
        if (Array.isArray(item) && n > 0) {
            result.push(...flat(item, n - 1));
        } else {
            result.push(item);
        }
    }
    return result;
}
```

* **Base Case:**  If `n` is 0 or the item is not an array, push it to the `result`.
* **Recursive Step:** If the item is an array and the depth (`n`) is greater than 0, recursively call `flat` on the nested array, decrementing `n`.

**Recursive BFS Solution**

```javascript
function flat(arr, n) {
    let result = [...arr]; // Start with a copy
    for (let depth = 0; depth < n; depth++) {
        const nextLevel = [];
        for (const item of result) {
            if (Array.isArray(item)) {
                nextLevel.push(...item);
            } else {
                nextLevel.push(item);
            }
        }
        result = nextLevel; 
    }
    return result;
}
```

* **Similar to Iterative BFS:**  This solution simulates the iterative approach using recursion.
* **Depth Tracking:** It explicitly tracks the current `depth` in a loop.

**Comparison**

| Approach          | Pros                                    | Cons                                               |
| ----------------- | --------------------------------------- | -------------------------------------------------- |
| Iterative BFS    | Very efficient (time and space)         | Less intuitive than recursion for some              |
| Recursive DFS    | Elegant and concise                     | Potentially higher space complexity due to recursion |
| Recursive BFS    | Similar to iterative, might be clearer for some | Potentially higher space complexity due to recursion |

**Choosing the Right Approach**

* **Iterative BFS:** Best for performance in most cases.
* **Recursive Solutions:** Might be easier to understand if you're comfortable with recursion. Consider the potential space complexity if dealing with very large arrays.

*/

var join = function (arr1, arr2) {
  const ret = new Map(); //map id to merged object
  const arr1map = arr1.reduce((map, obj) => {
    const { id, ...rest } = obj;
    map.set(id, rest);
    return map;
  }, new Map());
  const arr2map = arr2.reduce((map, obj) => {
    const { id, ...rest } = obj;
    map.set(id, rest);
    return map;
  }, new Map());

  for (let i = 0; i < arr1.length; i++) {
    // only arr1 has it so push all it's array
    if (!arr2map.has(arr1[i].id)) {
      ret.set(arr1[i].id, arr1[i]);
      //console.log(
      //  `id ${arr1[i].id} exists in array arr1 only, setting ret map at id ${arr1[i].id} to ${arr1[i]} `
      //);
    } else {

      ret.set(arr1[i].id, {});
      for (const key in arr1[i]) {
        //console.log(
        //  `id ${
        //    arr1[i].id
        //  } exists in both array, merging from arr1 key ${key} with value ${JSON.stringify(
        //    arr1[i][key],
        //    null,
        //    4
        //  )} `
        //);
        ret.get(arr1[i].id)[key] = arr1[i][key];
        //console.log(ret);
      }

    }
  }
  // console.log("merged map after processing arr1");
  // console.log(ret);

  // now process arr2
  for (let i = 0; i < arr2.length; i++) {
    if (!arr1map.has(arr2[i].id)) {
      ret.set(arr2[i].id, arr2[i]);
    } else {
      for (const key in arr2[i]) {
        ret.get(arr2[i].id)[key] = arr2[i][key];
      }
    }
  }

  ret_as_array = Array.from(ret.values());
  return ret_as_array.sort((a, b) => a.id - b.id);
};