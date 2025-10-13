// console.log('what happens when a thrown exception is not caught?');
// 
// throw new Error('an error has occurred');

// //answer:
// $ node throwVsExit.js 
// what happens when a thrown exception is not caught?
// ~/work/code/nodejs/tutorial/throwVsExit.js:3
// throw new Error('an error has occurred');
// ^
// 
// Error: an error has occurred
//     at Object.<anonymous> (~/work/code/nodejs/tutorial/throwVsExit.js:3:7)
//     at Module._compile (internal/modules/cjs/loader.js:956:30)
//     at Object.Module._extensions..js (internal/modules/cjs/loader.js:973:10)
//     at Module.load (internal/modules/cjs/loader.js:812:32)
//     at Function.Module._load (internal/modules/cjs/loader.js:724:14)
//     at Function.Module.runMain (internal/modules/cjs/loader.js:1025:10)
//     at internal/main/run_main_module.js:17:11
// $ echo $?
// 1
// 
//

console.log('its also possible to explicitly exit. e.g.');
process.exit(127);

// //ex:
// $ node throwVsExit.js 
// its also possible to explicitly exit. e.g.
// $ echo $?
// 127
