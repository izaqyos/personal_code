public class HelloWorldThreads extends Thread{

    public static void main(String[] args) {
        System.out.println("Running two threads to crunch some numbers...");
        Thread1 myThread1 = new Thread1();
        Thread2 myThread2 = new Thread2();
        myThread1.start();
        myThread2.start();

        System.out.println("Running two more threads to crunch some more numbers, this time the threads CTOR is passed a Runnable implementing class...");
        RunnableThread1 rt1 = new RunnableThread1();
        RunnableThread2 rt2 = new RunnableThread2();
        Thread t1 = new Thread(rt1);
        Thread t2 = new Thread(rt2);
        t1.start();
        t2.start();

        System.out.println("Illustrate that we cant call run directly. We need to call start to allocate a new call stuck and JVM calls run()");
        Thread3 myThread3 = new Thread3();
        myThread3.run();
    }
}
