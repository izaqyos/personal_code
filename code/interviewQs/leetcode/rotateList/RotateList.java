import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.lang.*; 

class ListNode
{
        private int val;
        private ListNode next = null;

        public ListNode getNext()
        {
                return this.next ;
        }

        public void setNext(ListNode next)
        {
                this.next = next;
        }

        public ListNode(int val)
        {
            this.val = val;
            next = null;
        }

        public String toString()
        {
                return String.valueOf(val);
        }

}

class LinkedList
{
        private ListNode head = null;
        private int size = 0;

        public String toString()
        {
                System.out.println("LinkedList toString called");

                ListNode ptmp = head;
                String sRet="";
                while (ptmp != null)
                {
                        sRet+= ptmp.toString();
                        if (ptmp.getNext() != null) sRet+="->";
                        ptmp = ptmp.getNext();
                }
                sRet+="|||";

                return sRet;
        } 

        public LinkedList(ListNode head)
        {
                this.head = head;
                while (head.getNext() != null) this.size++;
        }

        public LinkedList(ArrayList<Integer> arrL)
        {
                System.out.println("LinkedList CTOR called");
                ListNode tail = null;
                for (int val : arrL)
                {
                        ListNode lstNode = new ListNode(val);
                        if (head == null) 
                        {
                                System.out.println("LinkedList, add head "+val);
                                head = lstNode;
                                tail = head ;
                        }
                        else
                        {
                                System.out.println("LinkedList, add node "+val);
                                tail.setNext(lstNode);
                                tail = lstNode;
                        }
                }
                size = arrL.size();
                System.out.printf("LinkedList CTOR complete. size=%d%n", size);
        }

        public int getSize(){
                return size;
        }

        public ListNode getHead(){
                return head;
        }
}

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    boolean bDebug = false;
    public ListNode rotateRight(ListNode head, int k) {
            System.out.println("rotateRight() called") ;
            if (head == null || (head.getNext() == null)) 
            {
                    System.out.println("empty or single element list. return head") ;
                    return head;
            }

            LinkedList llist = new LinkedList(head);
            if (bDebug)
            {
                    System.out.printf("Rotating list: %s, by %d%n",head,k);
            }

            ListNode runner = head;
            ListNode tail = runner;
            System.out.printf("input list size is %d%n",llist.getSize()); 
            return head;
    }
}

public class RotateList
{
        public static void main (String[] args)
        {
                System.out.println("RotateList tester initialized");
                ListNode node1 = new ListNode(1);
                ListNode node2 = new ListNode(2);
                node1.setNext(node2);
                System.out.println("Manually created list: "+node1+"->"+node2+"|||");

                //LinkedList llist = new LinkedList(new ArrayList<>(1,2,3,4));
                ArrayList<Integer> nums  = new ArrayList<>();
                nums.addAll(Arrays.asList(1,2,3,4));
                
                LinkedList llist = new LinkedList(nums) ;
                System.out.println("created list: "+llist);

                List<Integer> emptyList = new ArrayList<>();
                List<Integer> ListJustZero = IntStream.range(0,1).boxed().collect(Collectors.toList()) ;
                List<Integer> ListZeroToOne = IntStream.range(0,2).boxed().collect(Collectors.toList()) ;
                List<Integer> ListZeroToTwo = IntStream.range(0,3).boxed().collect(Collectors.toList()) ;
                List<Integer> ListZeroToThree = IntStream.range(0,4).boxed().collect(Collectors.toList()) ;
                List<List<Integer>> ListOfRanges= new ArrayList<>();
                ListOfRanges.add(emptyList);
                ListOfRanges.add(ListJustZero);
                ListOfRanges.add(ListZeroToOne);
                ListOfRanges.add(ListZeroToTwo);
                ListOfRanges.add(ListZeroToThree);

                List<Integer> ks = Arrays.asList(0,2,1,3,20);
                int k = 0;
                List<LinkedList> listOfLinkedLists = new ArrayList<LinkedList>();

                for (List<Integer> lst : ListOfRanges){
                        System.out.println ("Rotating List= "+lst+", by "+Integer.toString(ks.get(k)));
                        listOfLinkedLists.add( new LinkedList((ArrayList<Integer>) ListOfRanges.get(k))) ;
                        Solution sol = new Solution();
                        sol.rotateRight( listOfLinkedLists.get(k).getHead(), ks.get(k));
                        k++;
                        System.out.println ("----------------------------------------------------------------------------------------------------");
                }
        }
}


