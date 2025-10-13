//https://stackoverflow.com/questions/4856717/javascript-equivalent-of-pythons-zip-functionhttps://stackoverflow.com/questions/4856717/javascript-equivalent-of-pythons-zip-function
//
const arr1 =  ['a', 'b', 'c,'];
const arr2 =  [1,2,3];
const arr3 =  ['a1','b2','c3'];
zip= rows=>rows[0].map((_,c)=>rows.map(row=>row[c])); //take rows as param, run on first array, for each element in 1st array run map to create array with elements from same index in all arrays
zipStep1 = rows=>console.log("rows[0] =", rows[0]);
zipStep2 = rows=>rows[0].map((_,c)=> console.log('mapping _ ',_ , ' and index ',c));
zipStep3 = rows=>rows[0].map((_,c)=>rows.map(row=> console.log('row[c] ', row[c])));

zipStep1([arr1, arr2, arr3]);
zipStep2([arr1, arr2, arr3]);
zipStep3([arr1, arr2, arr3]);
console.log('zip arr1: ', arr1, ' with arr2: ', arr2, ' result: ', zip([arr1, arr2]));
console.log('zip arr1: ', arr1, ' with arr2: ', arr2, ' with arr3: ', arr3, ' result: ', zip([arr1, arr2, arr3]));

