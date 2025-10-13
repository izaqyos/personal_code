
let delay = function (ms) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, ms);
    });
};

const fs = require('fs');

const readDir = (path) => {
    if (!path) {
        return Promise.reject("missing path...");
    }
    return new Promise((resolve, reject) => {
        fs.readdir(path, (err, files) => {
            if (err) {
                return reject(err);
            }
            resolve(files);
        });
    })
};

const readFile = (path) => {
    if (!path) {
        return Promise.reject("missing path...");
    }
    return new Promise((resolve, reject) => {
        fs.readFile(path, 'utf8', (err, content) => {
            if (err) {
                return reject(err);
            }
            resolve(content);
        });
    })
};

const x = {};

delay(100)
    .then((data) => {
        console.log("reading dir...");
        return readDir(__dirname);
    }).
    then((files) => {
        console.log('files:', files);
    })
    .catch((err) => console.error(`my final error handler: ${err}`));


async function boo() {
    await delay(100);
    console.log("reading dir...");
    try {
        const files = await readDir(__dirname);
        console.log('files:', files);
        return files;
    } catch(err) {
        console.error(`my final error handler: ${err}`);
    }
}

const path = require('path');

const readFiles = async (files) => {
    const result = [];
    // for (let i in files) {
    //     const file = await readFile(path.join(__dirname, files[i]));
    //     result.push(file);
    // }
    files.forEach(async (filename, i) => {
        console.log("i=", i);
        const file = await readFile(path.join(__dirname, filename));
        console.log("file:", file);
    });
    return result;
};

boo()
    .then(readFiles)
    .then((results) => console.log("results:", results))
    .then(() => console.log("done"));
