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
