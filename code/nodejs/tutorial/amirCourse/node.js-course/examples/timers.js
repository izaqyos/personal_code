function test() {
    setTimeout(function () {
        console.log("timeout");
    }, 0);

    setImmediate(function () {
        console.log("immediate");
    });

    process.nextTick(function () {
        console.log("nextTick");
    });
}

// Within main module context
// the execution of timers is non-deterministic
console.log("within main module:\n---------------");
test();

// Within an I/O cycle
// setImmediate executed first
var fs = require('fs');
fs.readFile(__filename, function () {
    console.log("\nwithin I/O cycle:\n---------------");
    test();

    // setImmediate vs. process.nextTick
    // setTimeout(function () {
    //     var count = 0;
    //     console.log("\nnextTick kills I/O:\n---------------");
    //     var rec = function () {
    //         var x = 100000;
    //         while (x--) x = x + 0;
    //         count % 10000 === 0 && console.log("In recursion...");
    //         count++ < 50000 && process.nextTick(rec); // try using setImmediate / process.nextTick
    //     };
    //     console.log("reading file");
    //     fs.readFile(__filename, function () {
    //         console.log("*** I/O finished ***");
    //     });
    //     console.log("calling recursion");
    //     rec();
    // }, 10);
});