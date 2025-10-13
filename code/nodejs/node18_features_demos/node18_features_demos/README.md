# node18 features with demos
NodeJS version 18 features demonstrated

*Note, End of security support Node 14. 30.4.2023*

# Recap major NodeJS 16 features 
## Platform support (apples M1)                                                                                                                                                                         
## V8 Ver 9
### RegExp match indices
### Faster Super
### WebAssembly
### Promise based timers
### AbortController/Signal
### WebCrypto
## ES 2021 support
## base64 utility methods

# Background
Node.js major release is updated every six months. The new release becomes the Current release for six months, which gives library authors time to add support for them.
After six months, odd-numbered releases, such as 17, become unsupported, and even-numbered releases, such as 16, move to the Active LTS (long-term support) status and are ready for general use. LTS release typically guarantees that critical bugs will be fixed for a total of 30 months. Production applications should only use Active LTS or Maintenance LTS releases.
Node.js 18 was released on April 19, 2022. It becomes the Current release. It comes with 5 major features:
* Experimental fetch API
* Web Streams API
* HTTP Timeouts
* Experimental test runner
* V8 JavaScript engine is updated to V8 10.1


# Fetch API arrives to Node
fetch finally arrives to NodeJS bringing uniformity with browsers

code example:
``` bash
[i500695@WYLQRXL9LQ:2023-01-29 17:37:23:~/work/code/nodejs/node18:]2085$ cat fetch.js
const url = 'https://jsonplaceholder.typicode.com/todos/1'
const getJsonFromUrl= async (url)  => {
console.log(`GET from ${url}`);
const resp = await fetch(url);
if (resp.ok) {
const jsonData = await resp.json();
console.log(`Got json ${JSON.stringify(jsonData, null, 4)} from ${url}`);
//console.log(`Got json ${JSON.stringify(jsonData, null, ' ')} from ${url}`);
//console.log(`Got json ${JSON.stringify(jsonData, null, "\t")} from ${url}`);
}
else {
console.error(`Got error ${resp.status} ${resp.statusText}`);
}
}

getJsonFromUrl(url);
 ```
Run example: 
```bash 
[i500695@WYLQRXL9LQ:2023-01-29 17:37:26:~/work/code/nodejs/node18:]2086$ node !$
node fetch.js
GET from https://jsonplaceholder.typicode.com/todos/1
(node:1350) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
Got json {
"userId": 1,
"id": 1,
"title": "delectus aut autem",
"completed": false
} from https://jsonplaceholder.typicode.com/todos/1
```

Note:
* fetch only rejects on network errors. It does not reject on HTTP errors.
* need to check response.ok and when not ok response.status response.statusText
* initial fetch response contains headers and more info but doesn't yet contain the body (since it needs to be gathered from the underlying TCP stream and marshalled + parsed)
```bash
interface Response extends Body {
readonly headers: Headers;
readonly ok: boolean;
readonly redirected: boolean;
readonly status: number;
readonly statusText: string;
readonly type: ResponseType;
readonly url: string;
clone(): Response;
}
 ```
* To get the JSON from body call .json() - which is asynchronous
* fetch is supported since 2015 on all browsers (- IE)
* In NodeJS it is based on https://undici.nodejs.org/#/ client lib
* fetch, FormData, Headers, Request, Response are now global objects in JavaScript

## webstreams API
Again, trying to make NodeJS streams more compatible with browser streams
Streams allow process in chunks instead of waiting for entire download of a resource (file, image, video etc) to complete, then deserialized into memory
Also streams allow detection of start/end and errors and can be canceled and chained

### Read Demo
```bash
[i500695@WYLQRXL9LQ:2023-01-29 18:54:57:~/work/code/nodejs/node18:]2090$ node readableStreamDemo.js
GET from https://jsonplaceholder.typicode.com/todos/1 using ReadableStream and ReadableStreamDefaultController
(node:3673) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
got response.body = ReadableStream { locked: false, state: 'readable', supportsBYOB: false }
streamReader= ReadableStreamDefaultReader {
stream: ReadableStream { locked: true, state: 'readable', supportsBYOB: false },
readRequests: 0,
close: Promise { <pending> }
}
controller= ReadableStreamDefaultController {}
ReadableStream { locked: false, state: 'readable', supportsBYOB: false }
false Uint8Array(83) [
123, 10,  32,  32,  34, 117, 115, 101, 114,  73, 100,  34,
58, 32,  49,  44,  10,  32,  32,  34, 105, 100,  34,  58,
32, 49,  44,  10,  32,  32,  34, 116, 105, 116, 108, 101,
34, 58,  32,  34, 100, 101, 108, 101,  99, 116, 117, 115,
32, 97, 117, 116,  32,  97, 117, 116, 101, 109,  34,  44,
10, 32,  32,  34,  99, 111, 109, 112, 108, 101, 116, 101,
100, 34,  58,  32, 102,  97, 108, 115, 101,  10, 125
]
Got stream done. Done state=true
result is: { userId: 1, id: 1, title: 'delectus aut autem', completed: false }
 ```
code:
```bash 
[i500695@WYLQRXL9LQ:2023-01-30 11:00:51:~/work/code/nodejs/node18:]2092$ cat readableStreamDemo.js |pbcopy
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
```

#### Code explanation
- use function arrow syntax: const getJsonFromUrl= (url)  => {
- call fetch: fetch(url).then( (resp) => {} which returns a promise which returns the response
- returns the response.body promise
  return resp.body;
- when response.body is ready handle it by extracting a ReadableStreamDefaultReader
  .then( responseBody => {
  const streamReader = responseBody.getReader();
  and return a new ReadableStream to process the stream:
  return new ReadableStream({
- The ReadableStream type has three optional callbacks. see:
```bash
  interface UnderlyingSource<R = any> {
  cancel?: UnderlyingSourceCancelCallback;
  pull?: UnderlyingSourcePullCallback<R>;
  start?: UnderlyingSourceStartCallback<R>;
  type?: undefined;
  }
  ``` 
- The ReadableStream in the example implements the start callback.
```bash
  start(controller) {
  start() receives a controller (of type ReadableStreamDefaultController)
  ``` 

- The controller can put data on stream Q and close it

  -- Put data in Q:
  controller.enqueue(value);
  -- Close stream
  controller.close();
- override push to define how data is processed
  function push() {
- Once the new ReadableStream is returned it's processed by
  .then((stream) => {

- which creates a Response w/ the stream content
  return new Response( stream, {
- And at last we print the response
  }).then ( result => {
  console.log('result is:', result); //the end result all the chunks parsed as json
  
### Other streams
* ReadableStream
* ReadableStreamDefaultReader
* ReadableStreamBYOBReader
* ReadableStreamBYOBRequest
* ReadableByteStreamController
* ReadableStreamDefaultController
* TransformStream
* TransformStreamDefaultController
* WritableStream
* WritableStreamDefaultWriter
* WritableStreamDefaultController
* ByteLengthQueuingStrategy
* CountQueuingStrategy
* TextEncoderStream
* TextDecoderStream
* CompressionStream
* DecompressionStream

## HTTP timeouts

There are two server side timeouts
for headers and for the whole request:
server.headersTimeout and server.requestTimeout
if they expire the server responds w/ 408 (the request will not be sent to RequestListener) and close connection
demo:


### side note import.meta
[official documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import.meta)                
import.meta
The import.meta meta-property exposes context-specific metadata to a JavaScript module. It contains information about the module, such as the module's URL.

Syntax
import.meta
Value
The import.meta object is created by the host environment, as an extensible null-prototype object where all properties are writable, configurable, and enumerable. The spec doesn't specify any properties to be defined on it, but hosts usually implement the following property:

url
The full URL to the module, includes query parameters and/or hash (following the ? or #). In browsers, this is either the URL from which the script was obtained (for external scripts), or the URL of the containing document (for inline scripts). In Node.js, this is the file path (including the file:// protocol).

Description
The import.meta syntax consists of the keyword import, a dot, and the identifier meta. Because import is a reserved word, not an identifier, this is not a property accessor, but a special expression syntax.

The import.meta meta-property is available in JavaScript modules; using import.meta outside of a module (including direct eval() within a module) is a syntax error.

#### Use for Passing query parameters
Using query parameters in the import specifier allows module-specific argument passing, which may be complementary to reading parameters from the application-wide window.location (or on Node.js, through process.argv). For example, with the following HTML:

```javascript

<script type="module">
  import "./index.mjs?someURLInfo=5";
</script>
```
The index.mjs module is able to retrieve the someURLInfo parameter through import.meta:

```javascript
// index.mjs
new URL(import.meta.url).searchParams.get("someURLInfo"); // 5
```
The same applies when a module imports another:

// index.mjs
```javascript
import "./index2.mjs?someURLInfo=5";
```

// index2.mjs
```javascript
new URL(import.meta.url).searchParams.get("someURLInfo"); // 5
```
The ES module implementation in Node.js supports resolving module specifiers containing query parameters (or the hash), as in the latter example. However, you cannot use queries or hashes when the module is specified through the CLI command (like node index.mjs?someURLInfo=5), because the CLI entrypoint uses a more CommonJS-like resolution mode, treating the path as a file path rather than a URL. To pass parameters to the entrypoint module, use CLI arguments and read them through process.argv instead (like node index.mjs --someURLInfo=5).

#### use to get current module's file path
In Node.js CommonJS modules, there's a __dirname variable that contains the absolute path to the folder containing current module, which is useful for resolving relative paths. However, ES modules cannot have contextual variables except for import.meta. Therefore, to get the current module's file path, you can use import.meta.url.


##### Before (CommonJS)

```javascript
const fs = require("fs/promises");
const path = require("path");

const filePath = path.join(__dirname, "someFile.txt");
fs.readFile(filePath, "utf8").then(console.log);
```

##### After (ES modules)
```javascript
import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";

const filePath = fileURLToPath(new URL('./someFile.txt', import.meta.url));
fs.readFile(filePath, "utf8").then(console.log);
```

### demo
#### Run:
``` javascript
[i500695@WYLQRXL9LQ:2023-02-01 16:57:16:~/work/code/nodejs/node18:]2007$ node httpTimeoutes.mjs
headersTimeout= 60000
requestTimeout= 300000
```

``` javascript
[i500695@WYLQRXL9LQ:2023-02-01 16:58:48:~/work/code/nodejs/node18:]2008$ cat !$
cat httpTimeoutes.mjs
import express from 'express';
import path, {dirname} from 'path';
import {fileURLToPath} from 'url';

const app = express();
const __dirname = dirname(fileURLToPath(import.meta.url));
app.use(express.static(path.join(__dirname, 'index.html')));

app.get('/*', (req, res) => {
setTimeout( () => res.sendFile(path.join(__dirname, './index.html')), 2000);
});

const server = app.listen(8080);
console.log('headersTimeout=', server.headersTimeout);
console.log('requestTimeout=', server.requestTimeout);
```

## Native Test Runner
import the new 'node:test' module.
Write UT and report results in TAP format (TAP= Test Anything Protocol)

Example tests run:

``` javascript
[i500695@WYLQRXL9LQ:2023-02-02 16:05:23:~/work/code/nodejs/node18:]2020$ node fetch-spec.mjs
GET from https://jsonplaceholder.typicode.com/todos/1
TAP version 13
Got json {
"userId": 1,
"id": 1,
"title": "delectus aut autem",
"completed": false
} from https://jsonplaceholder.typicode.com/todos/1
# Subtest: Standalone Test fetch positive
ok 1 - Standalone Test fetch positive
---
duration_ms: 112.746666
...
GET from null
got error TypeError, message Failed to parse URL from null
# Subtest: Nested Tests, fetch negatives
    # Subtest: Fetch null url
    ok 1 - Fetch null url
      ---
      duration_ms: 0.390417
      ...
GET from https://jsonplaceholder.typicode.com/todos/nonexistent
Got error 404 Not Found
got error Error, message Got error 404 Not Found
# Subtest: Fetch wrong url
ok 2 - Fetch wrong url
---
duration_ms: 29.089209
...
1..2
ok 2 - Nested Tests, fetch negatives
  ---
duration_ms: 29.896416
...
1..2
# tests 2
# pass 2
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 154.950833
```

Tests code:
``` javascript 
[i500695@WYLQRXL9LQ:2023-02-02 16:09:33:~/work/code/nodejs/node18:]2021$ cat fetch.mjs
const url = 'https://jsonplaceholder.typicode.com/todos/1'
export async function getJsonFromUrl(url){
console.log(`GET from ${url}`);
const resp = await fetch(url);
if (resp.ok) {
const jsonData = await resp.json();
console.log(`Got json ${JSON.stringify(jsonData, null, 4)} from ${url}`);
//console.log(`Got json ${JSON.stringify(jsonData, null, ' ')} from ${url}`);
//console.log(`Got json ${JSON.stringify(jsonData, null, "\t")} from ${url}`);
return jsonData;
}
else {
console.error(`Got error ${resp.status} ${resp.statusText}`);
throw new Error(`Got error ${resp.status} ${resp.statusText}`);
}
}


//getJsonFromUrl(url);
// module.exports={ getJsonFromUrl};
```

``` javascript 
[i500695@WYLQRXL9LQ:2023-02-02 16:09:38:~/work/code/nodejs/node18:]2021$ cat fetch-spec.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import {getJsonFromUrl} from './fetch.mjs';

test('Standalone Test fetch positive', async (t) => {
const url = 'https://jsonplaceholder.typicode.com/todos/1'
const expected = {
userId: 1,
id: 1,
title: "delectus aut autem",
completed: false
};
const data = await getJsonFromUrl(url);
assert.deepStrictEqual(data, expected);
});

test('Nested Tests, fetch negatives', async (t) => {
await t.test('Fetch null url', async (t) => {
const url = null;
await assert.rejects(
getJsonFromUrl(url),
err => {
console.log(`got error ${err.name}, message ${err.message}`); // would print got error TypeError, message Failed to parse URL from null
//assert.strictEqual(err.name, 'TypeError');
//assert.strictEqual(err.message, 'Failed to parse URL from null');
return true;
}
);
});
await t.test('Fetch wrong url', async (t) => {
const url =  'https://jsonplaceholder.typicode.com/todos/nonexistent';
await assert.rejects(
getJsonFromUrl(url),
err => {
console.log(`got error ${err.name}, message ${err.message}`); // would print got error TypeError, message Failed to parse URL from null
assert.equal(err.name, 'Error');
assert.equal(err.message, 'Got error 404 Not Found');
return true;
}
);
});
});
```



## V8 improvements  
### performance improvements:
For class fields and private class methods

### findLast and findLastIndex methods on arrays
``` javascript 
console.log('Array findLast and findLastIndex...');
const myArray = [
    {val: 1 },
    {val: 2 },
    {val: 3 },
    {val: 4 },
    {val: 5 },
    {val: 6 },
    {val: 7 },
    {val: 8 },
    {val: 9 },
    {val: 10},
    {val: 11},
];

console.log(`Find element divisible by 5 ${JSON.stringify(myArray.find( elem => elem.val %5 == 0))}`);
console.log(`Find last element divisible by 5 ${JSON.stringify(myArray.findLast( elem => elem.val %5 == 0))}`);
console.log(`Find index of element divisible by 5 ${myArray.findIndex( elem => elem.val %5 == 0)}`);
console.log(`Find index of last element divisible by 5 ${myArray.findLastIndex( elem => elem.val %5 == 0)}`);
console.log('--------------------------------------------------------------------------------');
```

### locale improvements
Intl.Locale (https://v8.dev/blog/v8-release-74#intl.locale) improvments (https://v8.dev/blog/v8-release-99#intl.locale-extensions)
  added properties calendars, collations, hourCycles, numberingSystems, timeZones, textInfo, and weekInfo.
Intl supportedValuesOf (https://v8.dev/blog/v8-release-99#intl-enumeration) 
code example:
```javascript
function printIntlLocaleDetails(localeStr) {
    console.log('Printing locale', localeStr);
    try {
        const locale= new Intl.Locale(localeStr);
        console.log(`${locale} details:`);
        console.log(`locale calendar: ${locale.calendars}, collations: ${locale.collations}, hourCycles: ${locale.hourCycles}, numberingSystems: ${locale.numberingSystems}, writing direction: ${JSON.stringify(locale.textInfo)}, week info: ${JSON.stringify(locale.weekInfo)}`);
        console.log('locale timeZones', locale.timeZones);
    }
    catch (err) {
        console.log(`cant init locale due to error ${err.name} ${err.message}`);
    }
}

```

```javascript
console.log('Locale improvements. get array of supported values in V8 for Intl APIs using Intl.supportedValuesOf(code). code can be calander, collation, currency, numberingSystems, timeZone etc');
console.log(Intl.supportedValuesOf('calendar'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('collation'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('currency'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('numberingSystem'));
await setTimeout(1000);
console.log('--------------------------------------------------------------------------------');
console.log(Intl.supportedValuesOf('timeZone'));
await setTimeout(1000);
```



