var fs = require("fs");
var data = '';

console.log("Provide stream result to a consumer");
let initStream = () => {
const readerStream = fs.createReadStream('input.txt');
readerStream.setEncoding('UTF8');
    return readerStream;
}

const provideResult = (stream) => {
    return new Promise((resolve, reject) => {
        const data = {};

        stream.on("data", () => {
            console.log('provideResult stream.on data ', data);
        });

        stream.on("end", () => {
            console.log('provideResult stream.on end. resolve promise');
            resolve(data);
        });

        stream.on("error", (err) => {
            console.log('provideResult stream.on error. reject promise');
            reject(err);
        });
    })
}

const consumeStream = () => {
    const stream = initStream();
    provideResult(stream);
}

consumeStream();


// const provideResult = (stream) => {
//     return new Promise((resolve, reject) => {
//         const data = {};
// 
//         stream.on("end", () => {
//             resolve(data);
//         });
// 
//         stream.on("error", (err) => {
//             reject(err);
//         });
//     })
// }
