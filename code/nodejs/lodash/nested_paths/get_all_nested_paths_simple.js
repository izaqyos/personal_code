const _ = require('lodash');
const getAllNestedPaths = (obj, prefix = []) => {
  return _.flatMapDeep(obj, (value, key) => {
    const path = [...prefix, key];
    return _.isObject(value) ? getAllNestedPaths(value, path) : path;
  });
};

// Example usage:
const obj = {
  foo: {
    bar: {
      baz: 42
    },
    qux: [1, 2, 3]
  },
  fizz: 'buzz'
};

const paths = getAllNestedPaths(obj);
console.log("Getting all paths of", obj); 
console.log(paths); // [['foo', 'bar', 'baz'], ['foo', 'qux'], ['fizz']]

