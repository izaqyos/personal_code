/**
 * Snippet 1.1: Event Loop, Microtasks (nextTick vs Promises), and Macrotasks
 *
 * Prediction Challenge:
 * Expected Output: 1 -> 9 -> 7 -> 5 -> 8 -> 6 -> 2 -> 3 -> 4
 *
 * Rules:
 * 1. Synchronous code executes first (1, 9).
 * 2. process.nextTick queue drains before Promise microtasks (7, then 5 & 8, then 6).
 * 3. Macrotask phases: Timers (setTimeout: 2 -> nextTick: 3), then Check (setImmediate: 4).
 */

console.log('--- 01: Event Loop & Microtasks ---');

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
