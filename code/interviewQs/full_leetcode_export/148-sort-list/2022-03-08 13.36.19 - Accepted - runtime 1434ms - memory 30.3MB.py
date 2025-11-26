# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self.mergeSort(head)

    def partition(self, head: Optional[ListNode]) -> Optional[ListNode]:
    #first partition starts at head, second at slow.next as slow ptr moves twice as slow as fast ptr he ends up in middle 
        if not head or not head.next:
            return head
        
        slow = head
        fast = head
        while (fast.next) and (fast.next.next):
            slow = slow.next
            fast = fast.next.next
        fast = slow.next 
        slow.next = None #break link between head tail (slow ptr) and right side partition list (slow.next which was stored in fast) , restore link in merge
        return fast #logically it's slow.next
        

    def merge(self, left: Optional[ListNode], right: Optional[ListNode]):
        print(f"merging {left.val} and {right.val}")
        returned_head = None
        ptr_to_last_elem_in_ret_list = None
        while left and right:
            if left.val <= right.val:
                if not returned_head:
                    returned_head = left 
                    ptr_to_last_elem_in_ret_list = left 
                    left = left.next 
                    ptr_to_last_elem_in_ret_list.next = None 
                else:
                    ptr_to_last_elem_in_ret_list.next = left
                    ptr_to_last_elem_in_ret_list = ptr_to_last_elem_in_ret_list.next
                    left = left.next
                    ptr_to_last_elem_in_ret_list.next = None
            else:
                if not returned_head:
                    returned_head = right 
                    ptr_to_last_elem_in_ret_list = right 
                    right = right.next 
                    ptr_to_last_elem_in_ret_list.next = None 
                else:
                    ptr_to_last_elem_in_ret_list.next = right 
                    ptr_to_last_elem_in_ret_list = ptr_to_last_elem_in_ret_list.next
                    right = right.next
                    ptr_to_last_elem_in_ret_list.next = None
        if left:
            ptr_to_last_elem_in_ret_list.next = left 
        if right:
            ptr_to_last_elem_in_ret_list.next = right

        return returned_head

        #run until shortest list ends. if elem in right < head 

    def printlist(self, head):
        while head:
            print(f"->{head.val}", end='')
            head = head.next
        print('|--')
        
    def mergeSort(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # empty or one elem is sorted, return 
        if (not head) or (not head.next):
            return head
        # partition list (use slow, fast pointers technique)
        right_list = self.partition(head)
        print(f"partition result. left starts at {head.val}, right starts at {right_list.val}")
        if right_list == head: #only happens for <2 elem lists and should be covered in  previous  check. just in case :)
            return head

        # mergeSort each partition 
        left = self.mergeSort(head)
        self.printlist(left)
        right = self.mergeSort(right_list)
        self.printlist(right)
        # merge the two partitions
        return self.merge(left, right)
