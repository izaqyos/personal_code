class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if (not head) or (not head.next):
            return False
        
        
        s=head
        f=head.next
        while s and s.next and f and f.next and f.next.next:
            s = s.next
            f= f.next.next
            if s==f:
                return True
        return False
