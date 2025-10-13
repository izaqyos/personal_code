var async_hooks = require('async_hooks');

//Async Hook implemented here

function print(displ){
    process._rawDebug(displ);
}

let map = new Map();
async_hooks.createHook({
    init: function(id, triggerAsyncId){
        let triggeredData = map.get(triggerAsyncId);
        if(triggeredData){
            map.set(id,triggeredData);
        }    
    },
    destroy: function(asyncId){
        //very important to delete it from map, to avoid memory leaks
        map.delete(asyncId);
    }
}).enable();

//express server creation script

const express = require('express');

const app = express();

app.use('/', (req,res,next)=>{
    
    req.corelationId="ABCDEFGHIJKL"

    map.set(async_hooks.executionAsyncId(), req);

    next();
})

app.get('/',(req,res)=>{

    setTimeout(()=>{
        setTimeout(()=>{
            setTimeout(()=>{
                setTimeout(()=>{
                  //  print(map);
                    print(`Get some asyncId 4>>>>> (${map.get(async_hooks.executionAsyncId()).corelationId})`); //ABCDEFGHIJKL
                    res.send("Hello world!!!!")
                },1000)
                setTimeout(()=>{
                   // print(map);
                    print(`Get some asyncId 4>>>>> (${map.get(async_hooks.executionAsyncId()).corelationId})`); //ABCDEFGHIJKL
                    //res.send("Hello world!!!!")
                },500)
            },1000)
        },1000)
    },1000)
        
});

app.listen(5000, ()=>{
    print("server started listening");
})
