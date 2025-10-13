var fs = require('fs');

fs.writeFile('message.txt', 'Hello Node js !!!', function (err) {
    if (err) throw err;
    console.log('File saved..');
    getFileContent('message.txt', function (fileContent) {
        console.log(fileContent);// 'Hello Node js !!!'
    });
});

function getFileContent(fileName, fnCallback) {
    fs.readFile(fileName, 'utf-8', function (err, content) {
        fnCallback(content);
    });
}
