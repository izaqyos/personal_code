var myarr;
myarr = [1, 2, 3];
console.log('myarr[0]=%d', myarr[0]);
var genArr = new Array(5);
for (var i = 0; i < genArr.length; i++) {
    genArr[i] = 'val' + i;
}
console.log('genArr[0]=%s', genArr[0]);
console.log("concat");
var concatArr = genArr.concat(genArr);
console.log("concatArr " + concatArr);
console.log("every");
var everyRetVal = concatArr.every(function (str) { return str.search('^val') != -1; });
console.log("everyRetVal " + everyRetVal);
console.log("array push/pop");
var poped = concatArr.pop();
concatArr.push(poped);
console.log("poped " + poped);
console.log("for in vs for of loop (index vs value)");
for (var elem in concatArr) {
    console.log('elem= ', elem);
}
for (var _i = 0, concatArr_1 = concatArr; _i < concatArr_1.length; _i++) {
    var elem = concatArr_1[_i];
    console.log('elem= ', elem);
}
