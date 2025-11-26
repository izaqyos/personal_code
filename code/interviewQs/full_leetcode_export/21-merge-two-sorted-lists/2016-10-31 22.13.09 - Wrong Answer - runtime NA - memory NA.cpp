/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        if ( (l1 == nullptr) && (l2 == nullptr)) return nullptr;
        if (l1 == nullptr) return l2;
        if (l2 == nullptr) return l1;
        
        ListNode * head = nullptr ; 
        ListNode * end = head;
        ListNode * temp = nullptr;
        while ( (l1 != nullptr) && (l2 != nullptr))
        {
            if ((l1->val) < (l2->val))
            {
                temp = l1;
                l1=l1->next;
            }
            else
            {
                temp = l2;
                l2=l2->next;
            }
            
            if (! head) 
            {
                head = temp;
                end = head;
            }
            else
            {
                end->next = temp;
                end = temp;
            }
            
        }
        
        while (l1 != nullptr) 
        {
            end->next = l1;
            l1 = l1->next;
        }
        
        while (l2 != nullptr)
        {
            end->next = l2;
            l2 = l2->next;          
        }
        
        return head;
        
    }
};