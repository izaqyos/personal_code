let fs = require("fs");


obj={
        'arr': ['a','b'],
        'innerObj': {
                'c': 1,
                'd': 'ddd'
        }
};

let buffer = new Buffer(JSON.stringify(obj, null, 4));
let filepath1='./fsDemoGeneratedOutput.json';
let filepath2='./fsDemoBufferedOutput.json';

console.log('async write buffer to file using low level api');
fs.open(filepath2, 'w', function(err, fd){
        if (err){
                throw 'error opening file '+ err;
        }

        fs.write(fd, buffer, 0, buffer.length, null, function(err){
                if (err){
                        throw 'error writing to file ' + err;
                }
                
                    fs.close(fd, function() {
                            console.log('finished writing. file closed.');
                    });
    })
});
console.log('finished async write buffer to file using low level api');

//now read back
fs.open(filepath2, 'r', function(err, fd){
        if (err){
                throw 'error opening file '+ err;
        }
                //at this point write has finished
                fs.read(fd, Buffer.alloc(300), 0, 300, 0, function(err, bytesRead, buf) {
                    if (err){
                            throw 'error reading from file ' + err;
                    }

                    console.log('read from file ');
                    console.log(buf.toString('utf8'));
                });
         fs.close(fd, function() {
                 console.log('finished reading. file closed.');
         });
});


console.log('async write JSON to file using higher level api');
fs.writeFile(filepath1, JSON.stringify(obj), 'utf8', function(err){
        if (err){
                console.log('fs.writeFile error '+err);
        }
        console.log('completed writing JSON to file');
});

setTimeout( function(){
        fs.readFile(filepath1, 'utf8' , function (err, data){
        if (err){
                console.log('fs.readFile error '+err);
        }
        let obj1 = JSON.parse(data); // convert to object just for kicks 

        console.log('readFile has read ', data);

        });
}, 1000);

console.log('async readdir, read all files in dir');
fs.readdir('.', (err, files) => {
    console.log('async readdir, files:');
  files.forEach(file => {
    console.log(file);
  });
});

console.log('sync readdir, read all files in dir');
let counter = 1;
fs.readdirSync('.').forEach(file => {
  console.log('sync read files: ', file);
    if (counter == 1){
        console.log('async read file: ', file);
        fs.readFile(file, 'utf8', function(err, contents) {
            console.log(contents);
        });

        console.log('sync read file: ', file);
        const contents1 = fs.readFileSync(file, 'utf8');
        console.log(contents1);
        counter++;
    }
});

