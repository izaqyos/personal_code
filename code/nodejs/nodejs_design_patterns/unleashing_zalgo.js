var fs = require('fs');
var cache = {};
function inconsistentRead(filename, callback) {
    if(cache[filename]) {
        //invoked synchronously
        console.log(`invoked synchronously for reading file ${filename}`);
        callback(cache[filename]);
    } else {
        //asynchronous function 
        console.log(`invoked asynchronously for reading file ${filename}`);
        fs.readFile(filename, 'utf8', function(err, data) {
            cache[filename] = data;
            callback(data);
        });
    }
}

function createFileReader(filename) {
    console.log(`creating a reader for file ${filename}`);
    var listeners = [];
    inconsistentRead(filename, function(value) {
        listeners.forEach(function(listener) {
            console.log(`updating listener ${listener} with value ${value}`);
            listener(value);
        });
    });
    return {
        onDataReady: function(listener) {
            listeners.push(listener);
        }
    };
}
// When the preceding function is invoked, it creates a new object that acts as a notifier,
// allowing to set multiple listeners for a file read operation. All the listeners will be
// invoked at once when the read operation completes and the data is available. The
// preceding function uses our inconsistentRead() function to implement this
// functionality. Let's now try to use the createFileReader() function:
//
var reader1 = createFileReader('data.txt');
reader1.onDataReady(function(data) {
    console.log('First call data: ' + data);//...sometime later we try to read again from
    //the same file
    var reader2 = createFileReader('data.txt');
    reader2.onDataReady(function(data) {
        console.log('Second call data: ' + data);
    });
});

