// File: demo/async_promise_exceptions.js

console.log("--- Starting async/promise error handling demo ---\n");
console.log("This script demonstrates 4 scenarios involving Promises and async/await error handling:\n");
console.log("1. Awaited promise throws in constructor => should be caught in try/catch.\n");
console.log("2. Non-awaited promise throws in constructor => will be unhandled (not caught).\n");
console.log("3. Awaited promise rejects via reject() => should be caught in try/catch.\n");
console.log("4. Async function throws => rejected promise, caught with await try/catch.\n");
console.log("Observe how errors propagate depending on whether promises are awaited and properly handled.\n\n");

// Scenario 1: Promise throws inside constructor, and is awaited
// The thrown error will reject the promise and propagate to the await
async function case1() {
  console.log("[Case 1] Starting...");
  try {
    await new Promise((resolve, reject) => {
      // Error thrown inside the promise constructor
      throw new Error("Case 1: Error thrown in promise (awaited)");
    });
  } catch (err) {
    // Catches the error from the rejected promise
    console.log("[Case 1] Caught error:", err.message);
  }
  console.log("[Case 1] Finished\n");
}

// Scenario 2: Promise throws inside constructor, but is NOT awaited
// The thrown error rejects the promise but since it's not awaited or caught, it's unhandled
async function case2() {
  console.log("[Case 2] Starting...");
  try {
    new Promise((resolve, reject) => {
      // Error thrown immediately when promise is created
      throw new Error("Case 2: Error thrown in promise (NOT awaited)");
    });
  } catch (err) {
    // This catch block doesn't catch it because the error happens asynchronously
    console.log("[Case 2] Caught error:", err.message);
  }
  console.log("[Case 2] Finished\n");
}

// Scenario 3: Promise rejects using reject(), and is awaited
// The reject call will cause the await to throw
async function case3() {
  console.log("[Case 3] Starting...");
  try {
    await new Promise((resolve, reject) => {
      // Explicit rejection
      reject(new Error("Case 3: Promise rejected (awaited)"));
    });
  } catch (err) {
    // Catches the error from the rejected promise
    console.log("[Case 3] Caught error:", err.message);
  }
  console.log("[Case 3] Finished\n");
}

// Scenario 4: async function throws
// This will create a rejected promise that must be awaited or caught
async function throwsAsync() {
  // Throwing inside an async function implicitly rejects the returned promise
  throw new Error("Case 4: Thrown from async function");
}

async function case4() {
  console.log("[Case 4] Starting...");
  try {
    // Awaiting a rejected async function
    await throwsAsync();
  } catch (err) {
    // Catches the rejection from the async function
    console.log("[Case 4] Caught error:", err.message);
  }
  console.log("[Case 4] Finished\n");
}

// Run all cases in sequence using an IIFE
(async function runAll() {
  await case1(); // Handle thrown inside promise and awaited
  await case2(); // Throws inside promise, but not awaited
  await case3(); // Rejected promise using reject(), awaited
  await case4(); // Rejection from async function
  console.log("--- All cases completed ---");
})();
