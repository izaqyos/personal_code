var message = "Hello World typescript. To install: $npm install -g typescript. To compile: $tsc file.ts. To run: $node file.js";
console.log(message);
var MyClass = /** @class */ (function () {
    function MyClass() {
    }
    MyClass.prototype.greet = function () {
        console.log("ts is OOP language");
    };
    MyClass.prototype.printTypes = function () {
        console.log("any for no type, number for both integers and fractions, string, boolean, void, null and undefined");
    };
    return MyClass;
}());
var instanceOfMyClass = new MyClass();
instanceOfMyClass.greet();
instanceOfMyClass.printTypes();
var declareTypeAndValue = "like this";
var declareTypeAndNoValue; //value is undefined
var declareValueAndNoType = "variable type is inferred from value";
var declareWithoutValueAndType; //type is any value is undefined
var aname = "John";
var score1 = 50;
var score2 = 42.50;
var sum = score1 + score2;
console.log("name" + aname);
console.log("first score: " + score1);
console.log("second score: " + score2);
console.log("sum of the scores: " + sum);
console.log("Type Assertion in TypeScript, like casting but for compile time");
var str = '1';
var str2 = str; //str is now of type number 
console.log(str2);
var global_num = 12; //global variable 
var Numbers = /** @class */ (function () {
    function Numbers() {
        this.num_val = 13; //class variable 
    }
    Numbers.prototype.storeNum = function () {
        var local_num = 14; //local variable 
    };
    Numbers.sval = 10; //static field 
    return Numbers;
}());
console.log("Global num: " + global_num);
console.log(Numbers.sval); //static variable  
var obj = new Numbers();
console.log("Global num: " + obj.num_val);
function afunc(anum, aname, optionalparam) {
    console.log("afunc() got: ", anum, aname, (optionalparam == undefined) ? "undefined" : optionalparam);
}
afunc(42, 'yosi');
console.log("rest parameters (...)");
function addNumbers() {
    var nums = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        nums[_i] = arguments[_i];
    }
    var i;
    var sum = 0;
    for (i = 0; i < nums.length; i++) {
        sum = sum + nums[i];
    }
    console.log("sum of the numbers", sum);
}
addNumbers(1, 2, 3);
addNumbers(10, 10, 10, 10, 10);
console.log("Function() constructor");
var myFunction = new Function("a", "b", "return a * b");
var x = myFunction(4, 3);
console.log(x);
console.log("recursion");
function factorial(number) {
    if (number <= 0) { // termination case
        return 1;
    }
    else {
        return (number * factorial(number - 1)); // function invokes itself
    }
}
;
console.log(factorial(6));
console.log("recursion of anonymous function");
(function () {
    var x = "Hello!!";
    console.log(x);
})(); // the function invokes itself using a pair of parentheses ()
console.log("lambda, aka fat arrow, function");
var foo = function (x) {
    x = 10 + x;
    console.log(x);
};
foo(100);
console.log("TypeScript Number Properties: ");
console.log("Maximum value that a number variable can hold: " + Number.MAX_VALUE);
console.log("The least value that a number variable can hold: " + Number.MIN_VALUE);
console.log("Value of Negative Infinity: " + Number.NEGATIVE_INFINITY);
console.log("Value of Negative Infinity:" + Number.POSITIVE_INFINITY);
