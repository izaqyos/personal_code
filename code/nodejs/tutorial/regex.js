const regexName = /^\w+$/

const testPatterns = ["a-c","$%", "abcd", "a_c", "a+b","a@b"];

let i;

for (i=0; i<testPatterns.length; i++)
{
        console.log("check pattern %s is a valid word. it is %s", testPatterns[i], regexName.test(testPatterns[i]));
}


//const regexFilename = /^\w+$/
//const filenameReservedRegex = require('filename-reserved-regex');
//console.log(" filenameReservedRegex=%s", filenameReservedRegex);
//const validFileName = require('valid-filename');

//const testFileNames=["abs.js","a..cpp","\a","a:b",">a","v<a","aaa", ".","..","a.","b..", ".a"]; 
//for (i=0; i<testFileNames.length; i++)
//{
//        console.log("check pattern %s is a valid filename. it is %s", testFileNames[i], validFileName(testFileNames[i]));
//}

//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
//
reDigits = /\d+/;
let res;
res = reDigits.exec('123 ddd');
console.log('reDigits.exec(\'123 ddd\'), %s', JSON.stringify(res, null, 4));
if (reDigits.test('a12d')){
        console.log('re test found match to reDigits');
}
if ('ff12dd'.match(reDigits)){
        console.log('string found match to reDigits');
}

//Todo, add demo for
//matchAll	A String method that returns an iterator containing all of the matches, including capturing groups.
//search	A String method that tests for a match in a string. It returns the index of the match, or -1 if the search fails.
//replace	A String method that executes a search for a match in a string, and replaces the matched substring with a replacement substring.
//split	A String method that uses a regular expression or a fixed string to break a string into an array of substrings.

console.log('replace examples...');
let src='https://a.b.com';
console.log('simple replace: ', src.replace('https','http'));
console.log('regex replace: ', src.replace(/^h\w+s/,'aaa'));
console.log('regex replace with lookahead: ', src.replace(/^h\w+s(?=:)/,'aaa'));
console.log('regex replace, can use capture groups: ', src.replace(/(http.*)(com)/,'$2-$1'));

