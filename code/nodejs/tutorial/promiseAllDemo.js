console.log('test Promise.all behaviour when one of the promises rejects w/o catch');

const simplePromise = (msg) => {
    return new Promise( (resolve, reject) => {
        // condition = true; //toggle resolve or reject
        const condition = false;
        console(`resolve/reject toggle flag is ${condition}`);
        if (condition) {
            resolve('resolved '+msg);
        }
        else {
            reject('rejected '+msg);
        }
    });
}
simplePromise('simple promise').then( (msg) => {
    console.log('fulfill promise using then. got msg: '+msg);
}).catch( (err) => {
    console.log('catch promise errors using catch. got error: '+err);
});

const resPromise = () => {
    return new Promise( (res, rej) => {
        setImmediate( () => {
            console.log('This promise resolves immediately');
            res('This promise resolves immediately');
        });
    })
}

const rejPromise = () => {
    return new Promise( (res, rej) =>{
        setTimeout( () => {
            console.log('This promise rejects after 1sec');
            rej('This promise rejects after 1sec');
        }, 1000);
    })
}

const rejCatchPromise = async () => {

    try{
        return await new Promise( (res, rej) =>{
            setTimeout( () => {
                console.log('This promise rejects after 1sec, try to catch');
                rej('This promise rejects after 1sec');
            }, 1000);
        })
    }
    catch(e){
        console.log('caught rejection');
        return 'caught rejection';
    }
}


const slowResPromise = () => {
    return new Promise( (res, rej) => {
        setTimeout( () => {
            console.log('This promise resolves after 3 sec');
            res('This promise resolves after 3 sec');
        }, 3000);
    })
}

mainCatch = async () => {
    const [resMsg, rejCatchMsg, slowResMsg ] = await Promise.all([
        resPromise(),
        rejCatchPromise(),
        slowResPromise()
    ]);

    console.log('res promise messages: ', resMsg);
    console.log('rej catch promise messages: ', rejCatchMsg);
    console.log('slow res promise messages: ', slowResMsg);
}

main = async () => {
    const [resMsg, rejMsg, slowResMsg ] = await Promise.all([
        resPromise(),
        rejPromise(),
        slowResPromise()
    ]);

    console.log('res promise messages: ', resMsg);
    console.log('rej promise messages: ', rejMsg);
    console.log('slow res promise messages: ', slowResMsg);
}

mainCatch();
//main(); //unhandled rejection... [i500695@C02X632CJGH6:2019-09-05 13:42:57:~/work/code/nodejs/tutorial:]2005$ node promiseAllDemo.js 
////test Promise.all behaviour when on of the promises rejects
////(node:10477) UnhandledPromiseRejectionWarning: ReferenceError: msgs is not defined
////    at main (/Users/i500695/work/code/nodejs/tutorial/promiseAllDemo.js:34:39)
////    at processTicksAndRejections (internal/process/next_tick.js:81:5)
////    at process.runNextTicks [as _tickCallback] (internal/process/next_tick.js:51:3)
////    at Function.Module.runMain (internal/modules/cjs/loader.js:865:11)
////    at internal/main/run_main_module.js:21:11
////(node:10477) UnhandledPromiseRejectionWarning: Unhandled promise rejection. This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch(). (rejection id: 1)
////(node:10477) [DEP0018] DeprecationWarning: Unhandled promise rejections are deprecated. In the future, promise rejections that are not handled will terminate the Node.js process with a non-zero exit code.
////[i500695@C02X632CJGH6:2019-09-05
