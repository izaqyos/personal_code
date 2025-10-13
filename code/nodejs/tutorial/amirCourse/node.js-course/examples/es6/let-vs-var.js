function loop() {
    for (var i = 0; i < 5; ++i) {
        setTimeout(function () {
            console.log(i); // output '5' 5 times
        }, 100);
    }

    for (let i = 0; i < 5; ++i) {
        setTimeout(function () {
            console.log(i); // output 0, 1, 2, 3, 4
        }, 100);
    }
}

function scoping() {
    let y = 0;

    if (y) {
        var myVar = 1;
    }
    console.log("using var:", myVar === 1);// > false

    if (y) {
        let myLet = 1;
    }
    console.log("using let:", myLet === 1);// > Uncaught ReferenceError: myLet is not defined
}