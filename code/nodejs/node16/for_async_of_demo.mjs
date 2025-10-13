// import fetch from 'node-fetch'; // node ver < 18
/* 
generator stream reader
 */
async function* streamAsyncIterable(stream){
    const reader = stream.getReader();//for native fetch once  it is supported in node
    // const reader = stream; //for node-fetch package
    try {
        while(true){
            const {done, val} = await reader.read();
            if (done) return;
            yield val;
        }
    } finally {
        reader.realeaseLock();
        console.log('read stream complete');
    }
}

//use it to read
//https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json

async function readResponseInChunks(url) {
    const resp = await fetch(url);
    let respSize = 0;
    let chunkNum = 0;
    for await (const chunk of streamAsyncIterable(resp.body)) {
        if (chunk) {
            respSize += chunk.length;
            console.log(`chunk {chunkNum}: {chunk}`);
            console.log(`Total size {respSize} bytes`);
        }
        else {
            console.log('got empty chunk');
        }
        console.log('----------');
    }
    console.log(`Total size {respSize} bytes`);
    return respSize;
}

// readResponseInChunks('https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json');
readResponseInChunks('https://jsonplaceholder.typicode.com/photos');
