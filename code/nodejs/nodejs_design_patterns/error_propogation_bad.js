var fs = require('fs');
console.log('demo what happens when an error is not caught in async method. It is thrown and ends up in event loop. Causing abort with uncaught exception');
function readJSONThrows(filename, callback) {
    fs.readFile(filename, 'utf8', function(err, data) {
            if(err)
            return callback(err);
            //no errors, propagate just the data
            callback(null, JSON.parse(data));
            });
};

readJSONThrows('data.txt', function(err) {
console.log(err);
});

console.log('This exception can not be caught by wrapping with try catch since the exception has different call stack and bubbles up to the event loop');
try {
    readJSONThrows('nonJSON.txt', function(err, result) {
        console.log(result);
    });
} catch(err) {
    console.log('This will not catch the JSON parsing exception');
}

console.log('the last stop before process is aborted is to handle the uncaughtException');
process.on('uncaughtException', function(err){
    console.error('This will catch at last the ' +
'JSON parsing exception: ' + err.message);
    //without this, the application would continue
    process.exit(1);
});

