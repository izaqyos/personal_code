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
    ListNode* deleteDuplicates(ListNode* head) {
        ListNode* A = head;
        if ( (A==NULL) || (A->next == NULL) ) return A;
    
    ListNode * pprev = A;
    ListNode * pcur = A->next;
    ListNode * ptemp = NULL;
    
    while (pcur)
    {
        /**
        if (pprev->val == pcur->val)
        {
            //ptemp = pcur;
            pprev->next = pcur->next;
            delete pcur;
            pcur = pprev->next; 
        }
        **/
        
        while (pprev->val == pcur->val)
        {
          ptemp = pcur;    
          pcur = pcur->next;
          delete ptemp;
          if (! pcur) return A;
        }
        
        if ( (pprev->next) != (pcur) ) //we skip one or more
        {
            pprev->next = pcur;
        }
    }
    
    return A;
    }
};