var fs = require("fs");
var data = '';

console.log("demo read stream. node streams emit data,end,error,finish events...");
// Create a readable stream
var readerStream = fs.createReadStream('input.txt');

// Set the encoding to be utf8. 
readerStream.setEncoding('UTF8');

console.log("reader register on data CB");
// Handle stream events --> data, end, and error
readerStream.on('data', function(chunk) {
   console.log("reader on data CB got chunk: ", chunk);
   data += chunk;
});

readerStream.on('end',function(){
   console.log("on end CB ");
   console.log(data);
});

readerStream.on('error', function(err){
   console.log("on error CB ");
   console.log(err.stack);
});


console.log("demo write stream.");
//var data1="sample data";

var writeStream = fs.createWriteStream('output.txt');

writeStream.write(data,'UTF8');
writeStream.end();

writeStream.on('finish', function () {
   console.log("writer got finish event");
});


writeStream.on('error', function (err) {
   console.log("writer got error event: ", err.stack);
});

console.log("Demo piping streams"); 
var readerStream1 = fs.createReadStream('input.txt');
var writeStream1 = fs.createWriteStream('piped_output.txt');
readerStream1.pipe(writeStream1);

console.log("check piped output..."); 
fs.readFile('piped_output.txt', function (err,data) {
    if (err) return console.error(err);
    console.log("Printing piped_output.txt from CB: ", data.toString());
});

console.log("Demo chaining streams"); 
console.log("Demo chaining streams. Compressing"); 
var zlib = require('zlib');


var readerStream2 = fs.createReadStream('input.txt');
readerStream2.
        pipe(zlib.createGzip()).
        pipe(fs.createWriteStream('input.txt.gz'));


readerStream2.on('end' , function (){
console.log("input.txt.gz created"); 

console.log("Demo chaining streams. Decompressing"); 
var readerStream3 = fs.createReadStream('input.txt.gz');
        readerStream3.
        pipe(zlib.createGunzip()).
        pipe(fs.createWriteStream('input1.txt'));

        readerStream3.on('end', function () {
            console.log("input.txt.gz decompressed to input1.txt"); 
            
        });
});

console.log("Program Ended");
