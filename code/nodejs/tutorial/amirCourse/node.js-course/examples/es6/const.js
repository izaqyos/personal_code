// const foo; // SyntaxError: missing = in const declaration

const bar = 123;
// bar = 456; // TypeError: `bar` is read-only

// NOT immutable:
const person = {
    name: 'Wes',
    age: 28
};
person.age = 29;



