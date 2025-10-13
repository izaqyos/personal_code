public class Thread3 extends Thread {

    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(String.format("Thread %d crunching input %d", Thread.currentThread().getId(), i));
            try {
                Thread.sleep(1000); // slow thread
            }
            catch (Exception e) {
                System.out.println("Caught exception "+ e);
            }
        }
    }

}