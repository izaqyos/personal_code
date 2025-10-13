import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class CompletableFutureDemo {
    public static void main(String[] args) throws Exception {
        
        // Factory methods
        CompletableFuture<Integer> completedFuture = CompletableFuture.completedFuture(42);
        CompletableFuture<String> failedFuture = CompletableFuture.failedFuture(new RuntimeException("Failed!"));

        // thenAcceptAsync with a custom executor
        Executor customExecutor = Executors.newSingleThreadExecutor();
        CompletableFuture<Void> thenAcceptAsyncDemo = completedFuture.thenAcceptAsync(result -> {
            System.out.println("Received result: " + result);
            System.out.println("Thread: " + Thread.currentThread().getName());
        }, customExecutor);

        // or method to handle the first completed future
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Result from Future 1");
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "Result from Future 2");
        CompletableFuture<String> firstCompleted = future1.thenCombine(future2, (res1, res2) -> res1+" | "+res2);
        firstCompleted.thenAccept( res3 -> System.out.println("Combined result of two futures: " + res3));

        // completeOnTimeout to handle a timeout
        CompletableFuture<Integer> delayedFuture = CompletableFuture.supplyAsync(() -> {
            try {
                TimeUnit.SECONDS.sleep(2); //simulate long running task
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return 100; //return value
        });

        CompletableFuture<Integer> result = delayedFuture.completeOnTimeout(42, 1, TimeUnit.SECONDS); // 42 is value to return on TO, 1 is TO, in seconds

        // delayedExecutor to introduce a delay
        Executor delayedExecutor = Executors.newScheduledThreadPool(1); // 1 thread in executor thread pool
        CompletableFuture<Void> delayedDemo = CompletableFuture.runAsync(() -> {
            try {
                TimeUnit.SECONDS.sleep(2); // this is the delay
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("Task executed after a delay."); // this is the task
        }, delayedExecutor);

        // Wait for completion
        thenAcceptAsyncDemo.get();
        System.out.println("First completed: " + firstCompleted.join());
        System.out.println("Timeout result: " + result.join());
        delayedDemo.get();
    }
}
