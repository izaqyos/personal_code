public class Thread2 extends Thread{

    public void run(){
        for (int i=0; i<100; i++) {
            System.out.println(String.format("Thread 2 crunching input %d", i));
            try {
                Thread.sleep(200); //faster thread, sleeps 200 ms
            }
            catch (Exception e) {
                System.out.println("Caught exception " + e);
            }
        }
    }

}