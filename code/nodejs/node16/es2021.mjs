console.log('string replaceALl now supported. No need to use regex or split and join');
const str='This is a demo string';
const str_with_commas=str.replaceAll(' ',',');
console.log(`replace all spaces in: ${str}. result is: ${str_with_commas}`);

const bignum=100_000_000_000;
console.log('can now represent nums with _ as separator. e.g. 100_000_000_000 value is:', bignum);



