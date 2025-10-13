const _ = require('lodash');
const getPathsForProperty = (obj, propName, prefix = []) => {
  return _.flatMapDeep(obj, (value, key) => {
    const path = [...prefix, key];
    if (_.isObject(value)) {
      return getPathsForProperty(value, propName, path);
    } else if (key === propName) {
      return {path, value};
    } else {
      return [];
    }
  });
};

// Example usage:
const obj = {
  foo: {
    id: 'fooId',
    bar: {
      id: 'barId',
      baz: {
        id: 'bazId'
      }
    }
  },
  fizz: {
    buzz: {
      id: 'buzzId'
    }
  }
};

console.log("getting all nested ids of", JSON.stringify(obj, null,4));
const paths = getPathsForProperty(obj, 'id');
console.log(paths);

