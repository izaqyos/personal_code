var myarr:number[];

myarr = [1,2,3];

console.log('myarr[0]=%d',myarr[0]);

var genArr:string[] = new Array(5);

for (var i=0; i<genArr.length;i++){
        genArr[i]='val'+i;
        }

console.log('genArr[0]=%s',genArr[0]);

console.log("concat");
var concatArr = genArr.concat(genArr);
console.log("concatArr "+concatArr);

console.log("every");
var everyRetVal = concatArr.every( str => str.search('^val') != -1);
console.log("everyRetVal "+everyRetVal);

console.log("array push/pop");
let poped  :string = concatArr.pop();
concatArr.push(poped);
console.log("poped "+poped);


console.log("for in vs for of loop (index vs value)");
for( let elem in concatArr){
console.log('elem= ',elem);
}

for( let elem of concatArr){
console.log('elem= ',elem);
}
