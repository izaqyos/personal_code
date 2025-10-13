
console.log("importing http module and loading server");

var http =require("http");

http.createServer( function(request, response) {

    console.log("Sending HTTP header status 200 (ok) , type text/plain");
    response.writeHead(200, {'Content-Type':'text/plain'} ) ;


    console.log("Sending HTTP body status: Hello World nodejs  ");
    response.end('Hello World nodejs \n');
}).listen(8081);

console.log("server up. listen on http://127.0.0.1:8081/");

var fs = require("fs")

var data = fs.readFileSync('helloWorld.js');
console.log("Reading file synchronously. content: ", data.toString());



console.log("Reading file asynchronously by registering a callback function to do something w/ file content...");
fs.readFile('helloWorld.js', function (err,data) {
    if (err) return console.error(err);

    console.log("Printing file content from CB: ", data.toString());
});

console.log("End of demo program");



