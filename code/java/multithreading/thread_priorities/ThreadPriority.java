// Java Program to illustrate Priority Threads
// Case 1: No priority is assigned (Default priority)

// Importing input output thread class
import java.io.*;
// Importing Thread class from java.util package
import java.util.*;

// Class 1
// Helper Class (Our thread class)
class MyThread extends Thread {

	public void run()
	{

		// Printing the current running thread via getName()
		// method using currentThread() method
		System.out.println("Running Thread : "
						+ currentThread().getName());

		// Print and display the priority of current thread
		// via currentThread() using getPriority() method
		System.out.println("Running Thread Priority : "
						+ currentThread().getPriority());
	}
}

class DefaultPriority {

	// Main driver method
	public static void main(String[] args)
	{

		// Creating objects of MyThread(above class)
		// in the main() method
		MyThread t1 = new MyThread();
		MyThread t2 = new MyThread();

		t1.start();
		t2.start();
	}
}

class NormalPriority {

	// Main driver method
	public static void main(String[] args)
	{

		// Creating objects of MyThread(above class)
		// in the main() method
		MyThread t1 = new MyThread();
		MyThread t2 = new MyThread();

       // Setting priority to thread via NORM_PRIORITY
        // which set priority to 5 as default thread
        t1.setPriority(Thread.NORM_PRIORITY);
        t2.setPriority(Thread.NORM_PRIORITY);

		// Case 1: Default Priority no setting
		t1.start();
		t2.start();
	}
}

class MinPriority {

	// Main driver method
	public static void main(String[] args)
	{

		// Creating objects of MyThread(above class)
		// in the main() method
		MyThread t1 = new MyThread();
		MyThread t2 = new MyThread();

       // Setting priority to thread via NORM_PRIORITY
        // which set priority to 5 as default thread
        t1.setPriority(Thread.MIN_PRIORITY);
        t2.setPriority(Thread.MIN_PRIORITY);

		// Case 1: Default Priority no setting
		t1.start();
		t2.start();
	}
}

class MaxPriority {

	// Main driver method
	public static void main(String[] args)
	{

		// Creating objects of MyThread(above class)
		// in the main() method
		MyThread t1 = new MyThread();
		MyThread t2 = new MyThread();

       // Setting priority to thread via NORM_PRIORITY
        // which set priority to 5 as default thread
        t1.setPriority(Thread.MAX_PRIORITY);
        t2.setPriority(Thread.MAX_PRIORITY);

		// Case 1: Default Priority no setting
		t1.start();
		t2.start();
	}
}

