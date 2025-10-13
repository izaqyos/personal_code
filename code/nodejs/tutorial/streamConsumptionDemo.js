var fs = require("fs");

console.log("Provide stream result to a consumer");
let initStream = () => {
const readerStream = fs.createReadStream('input.txt');
readerStream.setEncoding('UTF8');
    return readerStream;
}

const provideResult = (stream) => {
    return new Promise((resolve, reject) => {
        let data = '';

        stream.on("data", (chunk) => {
            console.log('provideResult stream.on chunk ', chunk);
            data += chunk;
        });

        stream.on("end", () => {
            console.log('provideResult stream.on end. resolve promise');
            console.log('provideResult data ', data);
            resolve('here is data for consumer ' + data);
        });

        stream.on("error", (err) => {
            console.log('provideResult stream.on error. reject promise');
            reject(err);
        });
    })
}

const consumeStream = async () => {
    const stream = initStream();
    let result = await provideResult(stream);
    console.log('final result: ', result);
}

consumeStream();
