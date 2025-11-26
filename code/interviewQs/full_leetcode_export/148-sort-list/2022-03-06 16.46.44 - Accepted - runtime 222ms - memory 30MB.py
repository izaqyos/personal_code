# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        import heapq
        myheap = []
        cur = head
        while cur:
            heapq.heappush(myheap, cur.val)
            cur =cur.next
            
        cur = head
        while cur:
            cur.val = heapq.heappop(myheap)
            cur =cur.next
        
        return head