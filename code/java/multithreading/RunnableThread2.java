public class RunnableThread2 implements Runnable{

    public void run(){
        for (int i=0; i<4; i++) {
            System.out.println(String.format("RunnableThread 2 crunching input %d", i));
        }
    }
}
