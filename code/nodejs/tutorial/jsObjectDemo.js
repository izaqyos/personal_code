console.log('iterate object keys');
var data = {
  "VERSION": "2006-10-27.a",
  "JOBNAME": "EXEC_",
  "JOBHOST": "Test",
  "LSFQUEUE": "45",
  "LSFLIMIT": "2006-10-27",
  "NEWUSER": "3",
  "NEWGROUP": "2",
  "NEWMODUS": "640"
};

Object.keys(data).forEach(function(key) {
  console.log('Key : ' + key + ', Value : ' + data[key])
})

console.log('iterate array using forEach');
let arr = [1,2,3,4];
arr.forEach(function (arrayItem) {
    var x = arrayItem+ 2;
    console.log(x);
});


console.log('iterate array using for');
for (var j = 0; j < arr.length; j++){
  console.log(arr[j].x);
}


console.log('iterate array using for item');
for (let item of arr) {
    console.log(item); // Will display contents of the object inside the array
}

console.log('some use cases of looping through an array in the functional programming way in JavaScript');

//1. Just loop through an array

console.log('forEach loop');
let myArray = [{x:100}, {x:200}, {x:300}];

myArray.forEach((element, index, array) => {
    console.log(element.x); // 100, 200, 300
    console.log(index); // 0, 1, 2
    console.log(array); // same myArray object 3 times
});
//Note: Array.prototype.forEach() is not a functional way strictly speaking, as the function it takes as the input parameter is not supposed to return a value, which thus cannot be regarded as a pure function.

//2. Check if any of the elements in an array pass a test

console.log('filter using some()');
let  people = [
    {name: 'John', age: 23},
    {name: 'Andrew', age: 3},
    {name: 'Peter', age: 8},
    {name: 'Hanna', age: 14},
    {name: 'Adam', age: 37}];

const anyAdult = people.some(person => person.age >= 18);
console.log(anyAdult); // true
//3. Transform to a new array

myArray = [{x:100}, {x:200}, {x:300}];

console.log('generate an array using map()');
let newArray= myArray.map(element => element.x);
console.log(newArray); // [100, 200, 300]
//Note: The map() method creates a new array with the results of calling a provided function on every element in the calling array.

//4. Sum up a particular property, and calculate its average

console.log('sum an array using map() and reduce()');
myArray = [{x:100}, {x:200}, {x:300}];

const sum = myArray.map(element => element.x).reduce((a, b) => a + b, 0);
console.log(sum); // 600 = 0 + 100 + 200 + 300

const average = sum / myArray.length;
console.log(average); // 200
//5. Create a new array based on the original but without modifying it
console.log(' Create a new array based on the original but without modifying it');

myArray = [{x:100}, {x:200}, {x:300}];

newArray= myArray.map(element => {
    return {
        ...element,
        x: element.x * 2
    };
});

console.log(myArray); // [100, 200, 300]
console.log(newArray); // [200, 400, 600]
//6. Count the number of each category

console.log(' use reduce to count categories');
people = [
    {name: 'John', group: 'A'},
    {name: 'Andrew', group: 'C'},
    {name: 'Peter', group: 'A'},
    {name: 'James', group: 'B'},
    {name: 'Hanna', group: 'A'},
    {name: 'Adam', group: 'B'}];

const groupInfo = people.reduce((groups, person) => {
    const {A = 0, B = 0, C = 0} = groups;
    if (person.group === 'A') {
        return {...groups, A: A + 1};
    } else if (person.group === 'B') {
        return {...groups, B: B + 1};
    } else {
        return {...groups, C: C + 1};
    }
}, {});

console.log(groupInfo); // {A: 3, C: 1, B: 2}
//7. Retrieve a subset of an array based on particular criteria

console.log(' use filter() to retrueve a subset');
myArray = [{x:100}, {x:200}, {x:300}];

newArray = myArray.filter(element => element.x > 250);
console.log(newArray); // [{x:300}]
//Note: The filter() method creates a new array with all elements that pass the test implemented by the provided function.

//8. Sort an array
console.log(' use sort() ');

people = [
  { name: "John", age: 21 },
  { name: "Peter", age: 31 },
  { name: "Andrew", age: 29 },
  { name: "Thomas", age: 25 }
];

let sortByAge = people.sort(function (p1, p2) {
  return p1.age - p2.age;
});

console.log(sortByAge);

//9. Find an element in an array

console.log(' use find() ');
letpeople = [ {name: "john", age:23},
                {name: "john", age:43},
                {name: "jim", age:101},
                {name: "bob", age:67} ];

const john = people.find(person => person.name === 'john');
console.log(john);

//The Array.prototype.find() method returns the value of the first element in the array that satisfies the provided testing function.

let myObj={'k': 'val'};
console.log("initial object %s", JSON.stringify(myObj, null, 4));
myObj.inner = {'nested': 'value'};
let attr = 'newAttribute';
myObj.attr = ". notation will add the var name. oops";
myObj[attr] = "[] notation will add the var value. as expected";
console.log("object after adding attribute. %s", JSON.stringify(myObj, null, 4));

console.log('what happens when accessing nonexistent key');
try{
    myObj.l.s = 'this will not work!';
}
catch(e){
        console.log('error ',e);
}
console.log('did we get here?');


console.log('copy object properties from one or more sources to a target object. Object.assign(target, src1, src2, ...)');
console.log('Note that this is shallow clone so values that are inner objects are copied by reference');
function testCloning() {
  'use strict';

  let obj1 = { a: 0 , b: { c: 0}};
  let obj2 = Object.assign({}, obj1);
  console.log(' obj2 was empty. after assign of obj1:'); 
  console.log(JSON.stringify(obj2)); // { a: 0, b: { c: 0}}

  obj1.a = 1;
  console.log('obj1.a was changed. obj1,obj2:'); 
  console.log(JSON.stringify(obj1)); // { a: 1, b: { c: 0}}
  console.log(JSON.stringify(obj2)); // { a: 0, b: { c: 0}}

  obj2.a = 2;
  console.log('obj2.a was changed. obj1,obj2:'); 
  console.log(JSON.stringify(obj1)); // { a: 1, b: { c: 0}}
  console.log(JSON.stringify(obj2)); // { a: 2, b: { c: 0}}

  obj2.b.c = 3;
  console.log('obj2.b.c was changed. now notice the effect of shallow clone. obj1,obj2:'); 
  console.log(JSON.stringify(obj1)); // { a: 1, b: { c: 3}}
  console.log(JSON.stringify(obj2)); // { a: 2, b: { c: 3}}

  // Deep Clone
  obj1 = { a: 0 , b: { c: 0}};
  let obj3 = JSON.parse(JSON.stringify(obj1));
  obj1.a = 4;
  obj1.b.c = 4;
  console.log('obj3 is deep clone of obj1 so nested objects have different references than in obj1');
  console.log(JSON.stringify(obj3)); // { a: 0, b: { c: 0}}
}

testCloning();
