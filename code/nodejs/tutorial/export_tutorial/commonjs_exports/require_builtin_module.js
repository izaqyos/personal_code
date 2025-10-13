const fs = require('fs');
const path = require('path');
const folderPath = __dirname;

console.log('pwd: '+ folderPath);
fs.readdir(folderPath, (err, files) => {
  files.forEach(file => {
    console.log(file);
  });
});

