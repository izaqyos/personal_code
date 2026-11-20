/**
 * Challenge: Async Concurrency Limiter (Task Pool / p-limit)
 *
 * Goal: Implement an async task queue that restricts the maximum number
 * of concurrent promises running at any given time.
 *
 * Requirements:
 * 1. `add(task)`: Accepts a function returning a Promise<T>, queues it, and resolves with T when complete.
 * 2. Concurrency limit: At no point should more than `concurrency` tasks be active simultaneously.
 * 3. Preserve order of individual resolutions (each task's promise resolves with its own result).
 * 4. Error isolation: If one task rejects, it should reject its specific promise without crashing the queue.
 * 5. (Bonus): `activeCount` and `pendingCount` getters.
 */

export interface Task<T> {
  (): Promise<T>;
}

export class AsyncPool {
  private concurrency: number;
  private active: number = 0;
  private queue: Array<() => void> = [];
  private maxQSize = 100;

  constructor(concurrency: number) {
    if (concurrency < 1) {
      throw new Error('Concurrency must be at least 1');
    }
    this.concurrency = concurrency;
  }

  get activeCount(): number {
    return this.active;
  }

  get pendingCount(): number {
    return this.queue.length;
  }

  /**
   * Adds an async task to the pool and returns a Promise that resolves
   * with the task result when executed.
   */
  async add<T>(task: Task<T>): Promise<T> {
    // TODO: Implement task queueing and concurrency control
    if (this.active >= this.concurrency) {
      if (this.queue.length > this.maxQSize) {
        throw new Error('Queue is full');
      }
      console.log(`waiting for available slot, current active = ${this.active} , pending = ${this.queue.length} `);
      await new Promise<void>((res) => {
        this.queue.push(res);
      });
    }

    this.active++;
    try {
      return await task();
    } finally {
      this.active--;
      const toRes = this.queue.shift();
      toRes?.();
    }
  }

}

// -------------------------------------------------------------
// Test Harness (Run with: npx tsx 04_concurrency_pool.ts)
// -------------------------------------------------------------
async function runTests() {
  console.log('--- Testing AsyncPool (Concurrency Limit = 2) ---');

  const pool = new AsyncPool(2);
  let maxConcurrentObserved = 0;
  let currentlyRunning = 0;

  const createMockTask = (id: number, durationMs: number) => {
    return async () => {
      currentlyRunning++;
      maxConcurrentObserved = Math.max(maxConcurrentObserved, currentlyRunning);
      console.log(`[Start] Task ${id} (Active: ${currentlyRunning}, Pending: ${pool.pendingCount})`);

      await new Promise((r) => setTimeout(r, durationMs));

      currentlyRunning--;
      console.log(`[Done]  Task ${id} (Active: ${currentlyRunning})`);
      return `Result ${id} `;
    };
  };

  const startTime = Date.now();
  const tasks = [
    pool.add(createMockTask(1, 100)),
    pool.add(createMockTask(2, 100)),
    pool.add(createMockTask(3, 100)),
    pool.add(createMockTask(4, 100)),
  ];

  const results = await Promise.all(tasks);
  const totalTime = Date.now() - startTime;

  console.log('\n--- Verification Results ---');
  console.log('Results:', results);
  console.log(`Max concurrent observed: ${maxConcurrentObserved} (Expected: <= 2)`);
  console.log(`Total duration: ~${totalTime} ms(Expected: ~200ms with concurrency 2)`);

  if (maxConcurrentObserved <= 2 && totalTime >= 190 && results.length === 4) {
    console.log('✅ PASS: Concurrency limit respected!');
  } else {
    console.log('❌ FAIL: Concurrency limit or execution was not enforced.');
  }
}

if (require.main === module) {
  runTests().catch(console.error);
}
