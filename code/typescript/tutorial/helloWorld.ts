var message: string = "Hello World typescript. To install: $npm install -g typescript. To compile: $tsc file.ts. To run: $node file.js. use ts-node to compile and run"
console.log(message)

class MyClass{
    greet():void{
        console.log("ts is OOP language")
    }

    printTypes(): void{
        console.log("any for no type, number for both integers and fractions, string, boolean, void, null and undefined")
    }
}

var instanceOfMyClass = new MyClass()
instanceOfMyClass.greet()
instanceOfMyClass.printTypes()

var declareTypeAndValue: string = "like this";
var declareTypeAndNoValue: string ; //value is undefined
var declareValueAndNoType = "variable type is inferred from value" ; 
var declareWithoutValueAndType;  //type is any value is undefined

var aname:string = "John"; 
var score1:number = 50;
var score2:number = 42.50
var sum = score1 + score2 
console.log("name"+aname) 
console.log("first score: "+score1) 
console.log("second score: "+score2) 
console.log("sum of the scores: "+sum)

console.log("Type Assertion in TypeScript, like casting but for compile time")
var str = '1' 
var str2:number = <number> <any> str   //str is now of type number 
console.log(str2)

var global_num = 12          //global variable 
class Numbers { 
   num_val = 13;             //class variable 
   static sval = 10;         //static field 
   
   storeNum():void { 
      var local_num = 14;    //local variable 
   } 
} 
console.log("Global num: "+global_num)  
console.log(Numbers.sval)   //static variable  
var obj = new Numbers(); 
console.log("Global num: "+obj.num_val) 

function afunc(anum:number, aname:string, optionalparam?:string){
    console.log("afunc() got: ", anum, aname, (optionalparam == undefined) ? "undefined":optionalparam)
}

afunc(42, 'yosi')

console.log("rest parameters (...)") 
function addNumbers(...nums:number[]) {  
    var i;   
    var sum:number = 0; 
    
    for(i = 0;i<nums.length;i++) { 
       sum = sum + nums[i]; 
    } 
    console.log("sum of the numbers",sum) 
 } 
 addNumbers(1,2,3) 
 addNumbers(10,10,10,10,10)

console.log("Function() constructor") 
var myFunction = new Function("a", "b", "return a * b"); 
var x = myFunction(4, 3); 
console.log(x);

console.log("recursion") 
function factorial(number) {
    if (number <= 0) {         // termination case
       return 1; 
    } else {     
       return (number * factorial(number - 1));     // function invokes itself
    } 
 }; 
 console.log(factorial(6)); 

console.log("recursion of anonymous function"); 
 (function () { 
    var x = "Hello!!";   
    console.log(x)     
 })()      // the function invokes itself using a pair of parentheses ()

console.log("lambda, aka fat arrow, function"); 
 var foo = (x:number)=> {    
    x = 10 + x 
    console.log(x)  
 } 
 foo(100)

 console.log("TypeScript Number Properties: "); 
 console.log("Maximum value that a number variable can hold: " + Number.MAX_VALUE); 
 console.log("The least value that a number variable can hold: " + Number.MIN_VALUE); 
 console.log("Value of Negative Infinity: " + Number.NEGATIVE_INFINITY); 
 console.log("Value of Negative Infinity:" + Number.POSITIVE_INFINITY);
