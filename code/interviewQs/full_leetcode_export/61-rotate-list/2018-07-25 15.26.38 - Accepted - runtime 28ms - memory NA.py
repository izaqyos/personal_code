#!/bin/python

# Definition for singly-linked list.
class ListNode(object):

    def __init__(self, x):
        self.val = x
        self.next = None

def makeLinkedList(lst):
    head = None
    tail = None
    for n in lst:
        lstNode = ListNode(n)
        if head == None:
            head = lstNode
            tail = head
        else:
            tail.next = lstNode
            tail = lstNode

    return head

def prettyPrintLinkedList(head):
    while head != None:
        print"[{}]-->".format(head.val),
        head = head.next
    print ("|||");

class Solution(object):
    bDebug = False

    def rotateRight(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """

        if self.bDebug:
            print"Rotating by "+str(k)+" list :",
            prettyPrintLinkedList(head)

        if head == None:
            return head

        if (head.next == None):
            return head

        runner = head
        tail = runner
        size = 0
        while runner!= None: 
            size = size+1
            tail = runner 
            runner = runner.next


        if self.bDebug:
            print ("list size is {}, head={}, tail={}").format(size, head.val, tail.val)


        #Now that we know size we can normalize k (%n) and run n-k-1 steps to get to node before k, which would become new tail
        #note n-k-1 limits are 1<=k<=n-1 => max: n-1-1 (n>1 so >=0, node before last) , min: n-(n-1) -1 n-n+1-1 (head) 

        k = k%size
        if k==0:
            return head

        if self.bDebug:
            print("normalized k={}").format(k)

        steps = 0
        runner = head
        while steps < (size-k-1):
            steps = steps  +1
            runner = runner.next
            if self.bDebug:
                print("steps={}, runner={}").format(steps, runner.val)

        #At this point runner points to node immediatly before n-k 
        newHead = runner.next
        runner.next = None
        tail.next = head
        head = newHead 

        return head





def main():
    Cl1r = makeLinkedList(range(5))
    prettyPrintLinkedList(Cl1r)
    lists = [ [] , range(1), range(2) , range (6), range (10) ]

    print "original lists"
    for lst  in lists:
        prettyPrintLinkedList(makeLinkedList(lst))

    ks = [0,2,1,3,24]
    sol = Solution()
    for lst,k in zip (lists, ks):
        print ("rotating {} by {} ").format(lst, k)
        prettyPrintLinkedList( sol.rotateRight(makeLinkedList(lst),k) )


if  __name__=="__main__":
    main()




        