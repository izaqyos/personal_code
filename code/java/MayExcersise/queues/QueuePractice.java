package practice;

import java.util.Random;

public class QueuePractice{
	public static Queue copyQueue(Queue origQueue) { //פעולת עזר
		Queue retQ = new Queue();  

		
		Queue buQ =  new Queue();
		while(!origQueue.isEmpty()) {
			retQ.insert(origQueue.head()); 
			buQ.insert(origQueue.remove()); 
			}
		while(!buQ.isEmpty()) { 
			origQueue.insert(buQ.remove());
		}
		return retQ; 
	}

	public static boolean upQ(Queue <Integer> q) {
		if (q.isEmpty()) return true;
		Queue workQ = copyQueue(q);
		int max=(Integer)workQ.remove();
		while (!workQ.isEmpty()) {
			int value=(Integer)workQ.remove();
			if (value>=max) {
				max= value;
			}
			else return false;
		}
		return true;
	}
	
	public static boolean sidra(Queue <Integer> q) {
		if (q.isEmpty()) return false;
		Queue workQ = copyQueue(q);
		int min=(Integer)workQ.remove();
		int next=(Integer)workQ.remove();
		int d= min-next;
		if (d<=0) return false;
		while (!workQ.isEmpty()) {
			int value=(Integer)workQ.remove();
			if (next-value==d) {
				next= value;
			}
			else return false;
		}
		return true;
	}
	
	public static int findMax(Queue<Integer> intQ) { //פעולת עזר
		int max=intQ.head(); 
		while(!intQ.isEmpty()) {
			int value=intQ.remove(); 
			if(max<value) {
				max=value;
			}
		}
		return max;
	}
		
	public static Queue removeOneElement(Queue <Integer> q, Integer elem) {
		System.out.println("removeOneElement");
		Queue<Integer> retQ = new Queue<Integer>();
		while (!q.isEmpty()) {
			Integer val = q.remove();
			System.out.println("Processing "+ val);
			if (val != elem) {
				retQ.insert(val);
			}
			else {
				break;
			}
			
	}
		while (!q.isEmpty()) {
			retQ.insert(q.remove());
		}
		
		System.out.println(retQ);
		System.out.println("----------");
		return retQ;
	
	}

	public static Queue uptodown(Queue <Integer> q) {
		Queue workQ = copyQueue(q);
		Queue retQ = new Queue();
		while (!workQ.isEmpty()) {
			System.out.println("----------");
			int value=findMax(workQ); 
			retQ.insert(value);
			workQ=copyQueue(removeOneElement(workQ,value));
			System.out.println("removed max " + value);
			System.out.println(workQ);
			System.out.println("----------");
		}
		return retQ;
	}

	public static void main(String[] args) {
		System.out.println("QueueProject");
		Queue q =  new Queue();
		Random rnd=new Random();
		for(int i=0; i< 8; i++)
			q.insert(rnd.nextInt(100));
		System.out.println(q);
		System.out.println(upQ(q));
		System.out.println(q);
		System.out.println(sidra(q));
		System.out.println("Sort Q");
		System.out.println(q);
		System.out.println(uptodown(q));



	}

}
