/**
 * Snippet 1.2: Async / Await and Promise Execution Flow
 *
 * Prediction Challenge:
 * Expected Output: D -> A -> C -> F -> H -> B -> G -> E
 *
 * Key Concepts:
 * 1. async functions execute synchronously up until the first `await` (A, then C).
 * 2. `await` pauses execution and registers the rest of the function (B) as a microtask.
 * 3. The executor function passed into `new Promise(...)` runs SYNCHRONOUSLY immediately (F).
 * 4. `.then()` callbacks are queued as microtasks (G).
 * 5. Synchronous stack completes (H).
 * 6. Microtasks drain (B, then G).
 * 7. Macrotasks (setTimeout: E).
 */

console.log('--- 02: Async / Await & Promises ---');

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
