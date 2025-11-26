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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        
        if (n < 0) return head;
        
        vector <ListNode *> vNodePtrs;
        ListNode * pCur=head;
        unsigned int size =0;
        while (pCur)
        {
            ++size;
            vNodePtrs.push_back(pCur);
            if ( (pCur->next == NULL) && (n<=size) ) 
            {
                // delete vNodePtrs[size -n]
                if (size == n)
                {
                    head = vNodePtrs[0]->next;
                    
                }
                else
                {
                    vNodePtrs[size - n -1]->next = vNodePtrs[size - n]->next; 
                    
                }
                delete vNodePtrs[size - n];
                
            }
            
            pCur = pCur->next;
        }
        return head;
    }
};