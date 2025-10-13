"""
Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.

 

Example 1:


Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]
Example 2:

Input: head = [5], left = 1, right = 1
Output: [5]
 

Constraints:

The number of nodes in the list is n.
1 <= n <= 500
-500 <= Node.val <= 500
1 <= left <= right <= n
 

Follow up: Could you do it in one pass?
"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not  head or right == left:
            return head
        sublisthead = None
        sublisttail =  []
        cur = head
        cur_index = 0
        while cur:
            cur_index+=1
            if cur_index == left:
                sublisthead = cur 
                sublisttail.append(cur)
                break
            cur = cur.next

        if sublisthead:
            cur = cur.next #cur.val already added to tail
            while cur:
                cur_index += 1
                sublisttail.append(cur)
                if cur_index == right:
                    break
                cur = cur.next

        swaps_num = (right-left+1)//2
        for i in range(swaps_num):
            print(f"left={sublisthead.val}, right={sublisttail[-1].val}")
            tempptr = sublisttail.pop()
            tempval = tempptr.val
            tempptr.val = sublisthead.val
            sublisthead.val = tempval
            sublisthead = sublisthead.next

        #while sublisthead and sublisttail and sublisthead.val<sublisttail[-1].val:
        #    #print(f"left={sublisthead.val}, right={sublisttail[-1].val}")
        #    tempptr = sublisttail.pop()
        #    tempval = tempptr.val
        #    tempptr.val = sublisthead.val
        #    sublisthead.val = tempval
        #    sublisthead = sublisthead.next

        return head




