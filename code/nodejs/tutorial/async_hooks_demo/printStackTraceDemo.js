const async_hooks = require('async_hooks');

async_hooks.createHook({ init, destroy }).enable();

const stackMap = new Map();

function init(asyncId, type, triggerId, resource){

    let parentStackTrace = stackMap.get(triggerId)||'';

    let currentStackTrace = {}

    Error.captureStackTrace(currentStackTrace);

    stackMap.set(asyncId, currentStackTrace.stack + parentStackTrace);

}

function destroy(asyncId){
    //needed to avoid memory leaks
     stackMap.delete(asyncId);
}

const getError = function (err){
    //const err = new Error(...args);
    err.stack += stackMap.get(async_hooks.executionAsyncId());
    return err;
}

let funcA= function(){
    setTimeout(()=>funcB(), 0)
}

let funcB = function(){
    setTimeout(()=>funcC(), 0)
}

let funcC = function(){
    setTimeout(()=>{
      try{
      throw new Error("NEW ERROR");
      }
      catch(err){
          console.log(getError(err))
      }
    }, 0)
}

funcA();
