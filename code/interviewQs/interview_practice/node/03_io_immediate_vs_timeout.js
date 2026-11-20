const fs = require('fs');

/**
 * Snippet 1.3: I/O Callback Phase Transitions (setImmediate vs setTimeout)
 *
 * Prediction Question:
 * Inside an I/O callback (like fs.readFile), which callback runs first?
 *
 * Libuv Phase Cycle:
 *  ┌───────────────────────────┐
 *  │ 1. Timers (setTimeout)    │ ◄─── (Will execute in the NEXT loop iteration)
 *  └─────────────┬─────────────┘
 *                │
 *  ┌─────────────▼─────────────┐
 *  │ 2. Pending Callbacks      │
 *  └─────────────┬─────────────┘
 *                │
 *  ┌─────────────▼─────────────┐
 *  │ 3. Poll / I/O Phase       │ ◄─── [WE ARE CURRENTLY HERE during fs callback]
 *  └─────────────┬─────────────┘
 *                │
 *  ┌─────────────▼─────────────┐
 *  │ 4. Check (setImmediate)   │ ◄─── (Next phase entered immediately after Poll!)
 *  └─────────────┬─────────────┘
 *                │
 *  ┌─────────────▼─────────────┐
 *  │ 5. Close Callbacks        │
 *  └───────────────────────────┘
 *
 * Answer: `setImmediate` is GUARANTEED to execute BEFORE `setTimeout` inside any I/O callback!
 */

console.log('--- 03: I/O Context (setImmediate vs setTimeout) ---');

fs.readFile(__filename, () => {
  console.log('1. Inside fs.readFile I/O callback (Poll phase)');

  setTimeout(() => {
    console.log('3. setTimeout (Timers phase - next iteration)');
  }, 0);

  setImmediate(() => {
    console.log('2. setImmediate (Check phase - immediately after poll)');
  });
});
