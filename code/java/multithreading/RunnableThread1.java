public class RunnableThread1 implements Runnable{

    public void run(){
        for (int i=0; i<4; i++) {
            System.out.println(String.format("RunnableThread 1 crunching input %d", i));
        }
    }

}