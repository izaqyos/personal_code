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
                if (bDebug) System.out.println("rotateRight() called") ;
                if (head == null || (head.next == null) || (k < 1) )
                {
                        System.out.println("empty or single element list. return head") ;
                        return head;
                }

                if (bDebug)
                {
                        System.out.printf("Rotating list: %s, by %d%n",head,k);
                }

                //invariant.  runner points to last scanned node. size is list size (we know its >= 1)
                ListNode runner = head;
                ListNode tail = runner;
                int size = 1;
                while (runner.next != null)
                {
                        size++;
                        runner = runner.next;
                }

                k%=size;
                if (k == 0) return  head;

                tail = runner;
                if (bDebug) System.out.printf("input list size is %d%n",size);

                runner = head;
                for (int i = 0; i < size -k -1; i++) {
                        runner = runner.next;
                }

                tail.next=head;
                head = runner.next;
                runner.next=null;
                return head;
        }
}