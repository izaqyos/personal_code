const url = 'https://jsonplaceholder.typicode.com/todos/1'
const getJsonFromUrl= (url)  => {
    console.log(`GET from ${url} using ReadableStream and ReadableStreamDefaultController`);
    fetch(url).then( (resp) => {
        console.log('got response.body =',resp.body); //should print got response.body =ReadableStream { locked: false, state: 'readable', supportsBYOB: false }
        return resp.body;
    })
    .then( responseBody => {
        const streamReader = responseBody.getReader();
        console.log('streamReader=', streamReader);
        // should print
        // streamReader= ReadableStreamDefaultReader {
        //   stream: ReadableStream { locked: true, state: 'readable', supportsBYOB: false },
        //   readRequests: 0,
        //   close: Promise { <pending> }

        // now return a ReadableStream
        return new ReadableStream({
            start(controller) {
                console.log('controller=', controller);

                // push is the chunk handler
                function push() {
                    //ReadableStreamDefaultReader promise return function w/ 2
                    //params. done - boolean (true when stream is done)
                    //Uint8Array - binary buffer
                    streamReader.read().then( ({done, value}) => {
                        if (done) {
                            console.log(`Got stream done. Done state=${done}`);
                            controller.close();
                            return;
                        }
                        controller.enqueue(value); //put current chunk in Q
                        console.log(done,value); //should print false and Uint8Array content
                        push(); //call push again to process next chunk
                    });

                }
                push(); //process first chunk and cont. until done

            },
        });
    })
    .then( stream => {
        console.log(stream)// will print ReadableStream { locked: false, state: 'readable', supportsBYOB: false}
        return new Response( stream, {
            headers: { 'Content-Type': 'application/json'},
        }).json();
    }).then ( result => {
        console.log('result is:', result); //the end result all the chunks parsed as json
    });
};

getJsonFromUrl(url);
