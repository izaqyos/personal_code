var fs = require('fs');
function readJSON(filename, callback) {
    fs.readFile(filename, 'utf8', function(err, data) {
        var parsed;
        if(err)
            //propagate the error and exit the current function
            return callback(err);
        try {
            //parse the file contents
            parsed = JSON.parse(data);
        } catch(err) {
            //catch parsing errors
            return callback(err);
        }
        //no errors, propagate just the data
        callback(null, parsed);
    });
};

readJSON('data.txt', ( err, data)=>{
    if (err) {
        console.log('failed to read file. got error', err);
    }
    else {
        console.log('File content:', data);
    }
});


