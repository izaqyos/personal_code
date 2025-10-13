// console.log('what happens when a thrown exception is not caught?');
// 
// throw new Error('an error has occurred');

// //answer:
// $ node throwVsExit.js 
// what happens when a thrown exception is not caught?
// /Users/i500695/work/code/nodejs/tutorial/throwVsExit.js:3
// throw new Error('an error has occurred');
// ^
// 
// Error: an error has occurred
//     at Object.<anonymous> (/Users/i500695/work/code/nodejs/tutorial/throwVsExit.js:3:7)
//     at Module._compile (internal/modules/cjs/loader.js:956:30)
//     at Object.Module._extensions..js (internal/modules/cjs/loader.js:973:10)
//     at Module.load (internal/modules/cjs/loader.js:812:32)
//     at Function.Module._load (internal/modules/cjs/loader.js:724:14)
//     at Function.Module.runMain (internal/modules/cjs/loader.js:1025:10)
//     at internal/main/run_main_module.js:17:11
// [i500695@C02X632CJGH6:2019-12-15 18:59:06:~/work/code/nodejs/tutorial:]2010$ echo $?
// 1
// 
//

console.log('its also possible to explicitly exit. e.g.');
process.exit(127);

// //ex:
// [i500695@C02X632CJGH6:2019-12-15 18:59:15:~/work/code/nodejs/tutorial:]2011$ node throwVsExit.js 
// its also possible to explicitly exit. e.g.
// [i500695@C02X632CJGH6:2019-12-15 19:01:16:~/work/code/nodejs/tutorial:]2012$ echo $?
// 127
