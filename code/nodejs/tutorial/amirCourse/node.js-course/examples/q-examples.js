var Q = require('q');

function doSomeAsync() {return Q.resolve();}
function doSomeMoreAsync() {return Q.resolve();}

doSomeAsync()
    .then(function (value) {
        throw new Error("Oops");
    }, function (error) {
        // We only get here if "doSomeAsync" fails
    });

doSomeAsync()
    .then(function (value) {
        throw new Error("Oops");
    }).catch(function (error) {
    // We get here with either
    // doSomeAsync's error or Oops's error
});


doSomeAsync()
    .then(function (result) {
        // do your magic
        doSomeMoreAsync()
            .then(function (resultOfMoreAsync) {
                //...
            });
    });

function getFileContent(path) {
    return Q.nfapply(fs.readFile, [path, "utf-8"]);
}

// var readFile = Q.denodeify(fs.readFile);
// readFile("path/to/file", "utf-8").then(/*...*/);
//
// var obj = {foo: function (arg, callback) {/*...*/}};
// var foo = Q.nbind(obj.foo, obj);
// foo("dummy-arg").then(/*...*/);

Promise.all([
    getFileContent("a.txt"),
    getFileContent("b.txt")
]).then(function ([a, b, ...rest]) {
    // results[0] - a
    // results[1] - b
});
