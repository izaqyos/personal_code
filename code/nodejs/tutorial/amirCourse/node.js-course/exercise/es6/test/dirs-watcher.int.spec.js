describe("dirs-watcher integration tests", function () {
    let fs = require('fs');
    let path = require('path');
    let assert = require('assert');
    let sinon = require('sinon');
    const { DirsWatcher } = require('../dirs-watcher');

    it('should watch on directory', async () => {
        const watcher = new DirsWatcher();
        let counter = 0;
        const file = path.join(__dirname, 'dummy.txt');
        watcher.on("change", () => counter++);

        watcher.start(__dirname);

        await touchFile(file, new Date().getTime());
        await delay(50);
        await touchFile(file, new Date().getTime());
        await delay(50);
        watcher.stop(__dirname);
        await touchFile(file, new Date().getTime());
        await delay(50);
        assert.equal(counter, 2);
    });

    function touchFile(filepath, content) {
        return new Promise((resolve, reject) => {
            fs.writeFile(filepath, content, (err) => {
                if (err) return reject(err);
                resolve();
            });
        });
    }

    function delay(ms) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, ms);
        });
    }

});