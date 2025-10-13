const _ = require('lodash');
const getAllNestedPaths = (obj, prefix = []) => {
  return _.flatMapDeep(obj, (value, key) => {
    const path = [...prefix, key];
    console.log(path);
    return _.isObject(value)
      ? getAllNestedPaths(value, path)
      : { path, value };
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
console.log(paths);

