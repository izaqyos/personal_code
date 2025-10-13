# node16
demos and code snippets re. node 16 features

# Main node 16 features

## Platform support (apples M1)
Apples M1 chips (arm based) support
Updated the minimum supported Xcode version to 11 and the GCC version for Linux and AIX platforms to 8.3.


## V8 Ver 9

### RegExp match indices
``` bash
[i500695@WYLQRXL9LQ:2022-04-26 15:58:55:~/git/portal-cf-transport-service:]2162$ node -v
v17.9.0
[i500695@WYLQRXL9LQ:2022-04-26 15:58:58:~/git/portal-cf-transport-service:]2163$ node
Welcome to Node.js v17.9.0.
Type ".help" for more information.
> const re=/(a+)(b*)/d
undefined
> const m = re.exec('aaab');
undefined
> m.indices[0]
[ 0, 4 ]
> m.indices[1]
[ 0, 3 ]
> m.indices[2]
[ 3, 4 ]
```

### Faster Super
Faster super property access
Accessing super properties (for example, super.x) has been optimized by using V8’s inline cache system and optimized code generation in TurboFan. With these changes, super property access is now closer to being on par with regular property access, as can be seen from the graphs below.

### WebAssembly
Faster JS-to-Wasm calls
V8 uses different representations for the parameters of WebAssembly and JavaScript functions. 
When JavaScript calls an exported WebAssembly function, the call goes through a so-called JS-to-Wasm wrapper,
responsible for adapting parameters from JavaScript land to WebAssembly land as well as adapting results in the opposite direction.
This comes with a performance cost, so calls from JavaScript to WebAssembly were not as fast as calls from JavaScript to JavaScript
To minimize this overhead the JS-to-Wasm wrapper can now be inlined at the call site, simplifying the code and removing this extra stack frame



### Promise based timers
### AbortController/Signal
Can now cancel promise after a set time or condition has happened

### WebCrypto
Node.js provides an implementation of the standard Web Crypto API

All of the new Web Crypto methods are available on the subtle interface

Why not just require('crypto’)?

WebCrypto is more cross platform/environment compatible

It is entirely promise based syntax (and async/await) as opposed to crypto mishmash of sync calls, streams and callbacks 

Supports Symmetric Key Algorithms, AES, HMAC etc

Supports Asymmetric Key Algorithms, RSA, ECDH


### End of security support Node 14. 30.4.2023


## deprecated
fs.rmdir no longer supported. Instead use fs.rm(dir, {recursive:true})

## ES 2021 support 
dashboard of nodejs supported features per version: https://node.green/

String Replace all

Numeric separators

Weak refs – great for in memory caches allows GC to clean up better

FinalizationRegistry (a destructor) – works well with weak refs

||= , a || = b

&&= , a &&= b

??= , a ??= b

demo:
``` bash
[i500695@WYLQRXL9LQ:2022-06-19 17:49:53:~/work/code/nodejs/node16:]2085$ cat !$
cat es2021.mjs
console.log('string replaceALl now supported. No need to use regex or split and join');
const str='This is a demo string';
const str_with_commas=str.replaceAll(' ',',');
console.log(`replace all spaces in: ${str}. result is: ${str_with_commas}`);
const bignum=100_000_000_000;
console.log('can now represent nums with _ as separator. e.g. 100_000_000_000 value is:', bignum);
[i500695@WYLQRXL9LQ:2022-06-19 17:49:58:~/work/code/nodejs/node16:]2086$ node !$
node es2021.mjs
string replaceALl now supported. No need to use regex or split and join
replace all spaces in: This is a demo string. result is: This,is,a,demo,string
can now represent nums with _ as separator. e.g. 100_000_000_000 value is: 100000000000
```

##         16.8.9 base64 utility methods 
Atob and btoa for encoding to/from base64

## 