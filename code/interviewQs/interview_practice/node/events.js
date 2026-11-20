console.log('Practice execution order understanding')
// predict print order, should be: 1,9 (sync), 7 (nextTick), 5 (microTask)
// 8 (microTask), 6 (microTask), 2(timer), 3(nextTick), 4 (setImmediate comes after setTimeout)
console.log('1');

setTimeout(() => {
  console.log('2');
  process.nextTick(() => console.log('3'));
}, 0);

setImmediate(() => {
  console.log('4');
});

Promise.resolve().then(() => {
  console.log('5');
  process.nextTick(() => console.log('6'));
});

process.nextTick(() => {
  console.log('7');
  Promise.resolve().then(() => console.log('8'));
});

console.log('9');

console.log('Practice Async Await')
async function async1() {
  console.log('A');
  await async2();
  console.log('B');
}

async function async2() {
  console.log('C');
}

console.log('D');

setTimeout(() => {
  console.log('E');
}, 0);

async1();

new Promise((resolve) => {
  console.log('F');
  resolve();
}).then(() => {
  console.log('G');
});

console.log('H');

