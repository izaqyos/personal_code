const encode_str = "SAP Raanana";
console.log('base64 encode', encode_str); 
const base64_str = atob(encode_str);
console.log('Encoded:', base64_str);
// const initial= btoa(base64_str); 
// console.log('decoded:', initial);
