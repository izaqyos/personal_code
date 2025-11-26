class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        sublisthead = None
        sublisttail =  []
        cur = head
        while cur:
            if cur.val == left:
                sublisthead = cur 
                sublisttail.append(cur)
                break
            cur = cur.next

        if sublisthead:
            cur = sublisthead.next 
            while cur:
                sublisttail.append(cur)
                if cur.val == right:
                    break
                cur = cur.next

        while sublisthead and sublisttail and sublisthead.val<sublisttail[-1].val:
            
            tempptr = sublisttail.pop()
            tempval = tempptr.val
            tempptr.val = sublisthead.val
            sublisthead.val = tempval
            sublisthead = sublisthead.next

        return head
