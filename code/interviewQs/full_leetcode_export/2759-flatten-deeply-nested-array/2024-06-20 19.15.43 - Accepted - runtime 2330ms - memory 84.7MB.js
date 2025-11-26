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