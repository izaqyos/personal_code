class MyError extends Error {
    constructor(args) {
        super(args);
        this.name = 'MyError';
        this.message = 'Default MyError message';
    }
}
async function bar() {
    throw new MyError();
}

async function foo() {
    try {
       return bar(); 
    }
    catch (err) {
        console.log(`got error ${err}`);

    }
}

async function fooawait_error(msg) {
    try {
       return await bar(); 
    }
    catch (err) {
        console.log(`got error ${err}`);

    }
}

async function main() {
    fooawait_error(); //error will be caught
    foo(); //error will not be caught since no await for bar
}

main();
