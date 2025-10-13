public class KillThread{

    static volatile boolean exit = false; // We need static scope since main is static
                                 // and we want to access exit from main
                                 
    public static void main(String[] args) {
        System.out.println("Main thread starting...");
        new Thread() {
            public void run(){
                System.out.println("In thread run()");
                while (!exit){
                    System.out.println("Thread working. waiting for exit flag to finish");
                }
                System.out.println("Thread got exit flag. quitting.");
            }
        }.start();

        try {
            Thread.sleep(500);
        } catch(InterruptedException e){
            e.printStackTrace();
        }
        
        exit = true;
        System.out.println("Exiting main thread");
    }

}
