"""
Given a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list.

Return the linked list sorted as well.

Example 1:

Input: 1->2->3->3->4->4->5
Output: 1->2->5
Example 2:

Input: 1->1->1->2->3
Output: 2->3
"""

import pdb
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def buildList(self, nums) -> ListNode:
        head = None
        cur = None
        for n in nums:
            if head == None:
                head = ListNode(n)
                cur = head
            else:
                cur.next = ListNode(n)
                cur = cur.next

        return head

    def printList(self, head: ListNode):
        print('|', end='')
        while head != None:
            print('{}->'.format( head.val), end='');
            head = head.next
        print('|', end='')
        print('')


    def deleteDuplicates(self, head: ListNode) -> ListNode:
        #pdb.set_trace()
        prev, cur = None, None

        while True: #delete dupes in prefix
            shouldDelete = False
            if (head == None) or (head.next == None):
                return head
            prev = head
            cur = head.next

            while (cur != None) and (prev.val == cur.val):
                shouldDelete = True
                prev = cur
                cur = cur.next

            if shouldDelete:
                head = cur
            else:
                break

        #now prev != cur, prev point to final head
        while cur != None:
            shouldDelete = False
            while (cur.next != None) and (cur.next.val == cur.val):
                shouldDelete = True
                cur = cur.next
            
            if shouldDelete:
                prev.next = cur.next #delete sames
                if cur.next != None:
                    if (cur.next.next != None) and (cur.next.val != cur.next.next.val):
                        #invariant is kept prev != cur. 
                        prev = cur.next
                        cur = cur.next.next 
                    else:
                        cur = cur.next
                else:
                    break
            else:
                prev = cur
                cur = cur.next
        
        return head

def test():

    #inputs = [
    #    [1,2,2],
    #]
    inputs = [
        [],
        [1],
        [1,2,2],
        [1,2,3,3,4,4,5],
        [1,1,1,2,3],
    ]

    sol = Solution()
    
    for inp in inputs:
        lst = sol.buildList(inp)
        print('original list')
        sol.printList(lst)
        lst = sol.deleteDuplicates(lst)
        print('remove dupes list')
        sol.printList(lst)


if __name__ == "__main__":
    test()


        