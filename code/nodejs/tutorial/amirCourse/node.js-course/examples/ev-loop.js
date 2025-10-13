console.log('script start');

setTimeout(function() {
    console.log('setTimeout');
}, 0);

process.nextTick(() => {
    console.log('nextTick');
}, 0);

Promise.resolve().then(() => {
    console.log('promise1');
}).then(() => {
    console.log('promise2');
});

console.log('script end');