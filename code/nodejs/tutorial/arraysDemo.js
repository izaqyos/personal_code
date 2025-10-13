let myarray1 = [] //create an empty array
let myarray2 = ['a', 'b'] //create a non empty array
let myarrayofarrays=[myarray1, myarray2]

let printArr = function(arr){
    arr.forEach(function(item, index, array) {
        console.log(item, index);
});

};
console.log("Print arrays:");
printArr(myarrayofarrays);

let first = myarray2[0];
let last = myarray2[myarray2.length -1];


console.log("arrays add/remove operations:");
let newLength = myarray2.push('c'); //add to end
let lastElem = myarray2.pop(); // remove from end
let firstElem = myarray2.shift(); // remove from front
newLength = myarray2.unshift('aa'); //add to end
newLength = myarray2.unshift('aaa'); //add to end

let posofaa=myarray2.indexOf('aa');
printArr(myarray2);

//myarray2 = [aaa, aa, b]
//

console.log("remove n items from position. splice(pos, n). removing aa:");
let removedItem = myarray2.splice(myarray2.indexOf('aa'), 1);
printArr(myarray2);


console.log("remove n items from position. splice(pos, n). of array in object:");
let myobj1 = {
        'names': ['yosi', 'deby', 'may', 'itay', 'kay', 'bel']
};
console.log("myobj1.names before remove = %s", JSON.stringify(myobj1,null,4));
myobj1.names.splice(myobj1.names.indexOf('bel'));
console.log("myobj1.names after remove = %s", JSON.stringify(myobj1,null,4));
console.log("myobj1.names after remove = %s", JSON.stringify(myobj1,null,4));

console.log("arrays shallow copy");
let myarray3 = myarray2.slice();
printArr(myarray3);

console.log("array as result of regex match");
// Match one d followed by one or more b's followed by one d
// Remember matched b's and the following d
// Ignore case
var myRe = /d(b+)(d)/i;
var myarray4  = myRe.exec('cdbBdbsbz');
printArr(myarray4);

//Delete from array using filter https://stackoverflow.com/questions/10024866/remove-object-from-array-using-javascript
console.log('using filter to delete from array');
let myarray5 = myarray2.filter( (elem) => { return elem !== 'aaa';}) ;
printArr(myarray5);

let arrOfObj = [ {'k1':'val', 'k2':'val2'} , {'k3':'val3', 'k4':'val4'}]
console.log('array of objects print as string: %s', arrOfObj.toString());
console.log('array of objects print as string using join:  %s', arrOfObj.join(", "));
console.log('array of objects print as string using JSON.stringify:  %s', JSON.stringify(arrOfObj));
let myobj = {
        'arr': arrOfObj
}
console.log('nested object print as string using JSON.stringify:  %s', JSON.stringify(myobj, null, 4));

console.log('array concat examples');
let letters = ['a', 'b', 'c'];
let numbers = [1, 2, 3];

letters.concat(numbers);
// result in ['a', 'b', 'c', 1, 2, 3]
//
let num1 = [1, 2, 3];
let num2 = [4, 5, 6];
let num3 = [7, 8, 9];

numbers = num1.concat(num2, num3);

console.log(numbers); 
// results in [1, 2, 3, 4, 5, 6, 7, 8, 9]

letters = ['a', 'b', 'c'];

alphaNumeric = letters.concat(1, [2, 3]);

console.log(alphaNumeric);
// results in ['a', 'b', 'c', 1, 2, 3]

num1 = [[1]];
num2 = [2, [3]];

numbers = num1.concat(num2);
numbersDeep = JSON.parse(JSON.stringify(num1.concat(num2)));

console.log(numbers);
// results in [[1], 2, [3]]

console.log('array concat makes shallow copy of elements');
// modify the first element of num1
num1[0].push(4);

console.log(numbers);
// results in [[1, 4], 2, [3]]

console.log('array deep copy, use JSON.parse(JSON.stringify()) plus concat ');
console.log(numbersDeep);

let myarray6 = [{'a':1},{'a':2}]
console.log('use map to modify values. Original array is ', myarray6);

let myarray7 =  myarray6.map(item => {
        item.a = item.a+5;
        return item;
});
console.log('used map to modify values. result array is ', myarray7);

let newarr = [1,2,3].map( i => {return i*i;} );
console.log('generate new array from array using map: ', newarr);

