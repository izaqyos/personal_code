const req = (msg, errMsg) => {
    return new Promise((resolve, reject) => {
        setImmediate(() => {
            if (errMsg) return reject(msg)
            resolve(msg)
        })
    })
}

const req2 = (msg, errMsg) => {
    return new Promise((resolve, reject) => {
        setImmediate(() => {
            if (errMsg) return reject(msg)
            resolve(msg)
        })
    })
}

const req3 = (msg, errMsg) => {
    return new Promise((resolve, reject) => {
        setTimeout( () => {
            if (errMsg) return reject(msg)
            resolve(msg)
        }, 1000);
    })
}


const requestWrapper = (req) => {
    return req.then((res) => { return { status: 'success', result: res }}, 
        (err) => { return   {status: "fail", result: err} }
    )};

const requestWrapperAA = async (req) => {
    let res;
    try{
        res = await req;
        return { status: 'success', result: res }
    }catch (err){
        return   {status: "fail", result: err} 
    }
};

const func = async () => {
    //const reqs = [
    //    requestWrapper(req("boo")),
    //    requestWrapper(req2("foo", "error")),
    //    requestWrapper(req3("foobar", "error")),
    //    requestWrapper(req3("foo3"))
    //]

    const reqs = [
        requestWrapperAA(req("boo")),
        requestWrapperAA(req2("foo", "error")),
        requestWrapperAA(req3("foobar", "error")),
        requestWrapperAA(req3("foo3"))
    ];

    const results = await Promise.all(reqs);
    return results;
}

const test = function(){

    const startTime = process.hrtime();
    func().then( (res) =>  {
        console.log('results: ',res);
        const endTime = process.hrtime(startTime);
        console.log('elapsed time %ds %dms', endTime[0], endTime[1]/1000000);
    } );

    const promiseAllNoStopOnReject = async ( promises) => {
        let results = await Promise.all( promises.map( async promise => {
            let res;
            try{
                console.log('await promise ', promise);
                res = await promise;
                return { status: 'success', result: res }
            }
            catch(err){
                return {status: "fail", result: err} 
            }
        }));
        return results;
    }

    const reqs = [ req("boo"), req2("foo", "error"), req3("foobar", "error"), req3("foo3") ];
    const startTime2 = process.hrtime();
    promiseAllNoStopOnReject(reqs).then( (res) =>  {
        console.log('promiseAllNoStopOnReject results: ',res);
        res.forEach( (result, index) => {
            if (result.status === 'success'){
                console.log('promise %d has succeeded', index);
            }
            else{
                console.log('promise %d has failed', index);
            }
        });
        const endTime = process.hrtime(startTime2);
        console.log('elapsed time %ds %dms', endTime[0], endTime[1]/1000000);
    } );
}

test()
