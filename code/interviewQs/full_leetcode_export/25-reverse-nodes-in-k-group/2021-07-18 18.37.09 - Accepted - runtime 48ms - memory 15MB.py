# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def revkstack(self, start, k):
        if not start or k <2:
            return None
        replace = []
        cur = start
        while len(replace) < k:
            if cur:
                replace.append(cur.val)
            else: #we hit end of list before k
                replace = []
                break
            cur = cur.next
        
        if not replace:
            return None
        else:
            cur = start
            while replace:
                if cur:
                    cur.val = replace.pop()
                    cur = cur.next
        return cur
        
    def revkO1(self, start, k):
        if not start:
            return None
        toreplace = k
        st = start
        while toreplace > 1:
            steps = toreplace-1
            last = None
            while steps>0:
                last = st.next
                steps-=1
            if last:
                #replace last and st. move st to st.next. toreplace-=2 
                pass
            else:
                #reverse back, call revk with k = steps+1
                pass
                
            
            
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        if k < 1:
            return head
        start = head
        while start:
            start = self.revkstack(start,k)
        return head
            