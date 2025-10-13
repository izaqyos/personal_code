import java.util.Queue;
import java.util.LinkedList; 

public class ChangeQOrder{

    public static void switchOrder(Queue<String> names, String deanSonName) {
        if (names.peek() == deanSonName) return;

        Queue<String> newQ = new LinkedList<>();
        String first = names.peek();
        names.remove();

        while (!names.isEmpty()) {
            if (names.peek() != deanSonName) {
                newQ.add(first);
                first = names.remove();
            }
            else { // we found dean son, let's switch
                newQ.add(names.remove());
                newQ.add(first);
                break;
            }
        }
        while (!names.isEmpty()) {
            newQ.add(names.remove());
        }

        //pretty print newq here
        while (!newQ.isEmpty()) {
            System.out.println(newQ.remove());
        }

        return;
    }

  public static void main(String[] args) {

Queue<String> nameQueue = new LinkedList<>();

System.out.println("The original queue is: ");
nameQueue.add("John");
System.out.println("John"); 

nameQueue.add("Jane"); 
System.out.println("Jane"); 
nameQueue.add("Bob");
System.out.println("Bob");  
nameQueue.add("Mary");
System.out.println("Mary");


System.out.println("Dean's son is Bob. The switched queue is: ");
switchOrder(nameQueue, "Bob");

  }

}
