public class Thread1 extends Thread {

    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(String.format("Thread 1 crunching input %d", i));
            try {
                Thread.sleep(1000); // slow thread
            }
            catch (Exception e) {
                System.out.println("Caught exception "+ e);
            }
        }
    }

}