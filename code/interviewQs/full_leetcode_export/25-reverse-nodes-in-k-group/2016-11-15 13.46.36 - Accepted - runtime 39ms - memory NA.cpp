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

    bool bDebug = false;
    void printNode(string msg, ListNode* node)
    {
        if (node)    cout<<msg<<node->val<<endl;
        
        else cout<<msg<<" null"<<endl;
        
    }
    
    ListNode* reverseKGroup(ListNode* head, int k) {
        if ((head == nullptr ) || (head->next == nullptr) || (k<2)      ) return head;
        
        ListNode* fakeHead = new ListNode(0);
        fakeHead->next = head;
        
        ListNode* prev= fakeHead,*cur = fakeHead; // fake head so we don't have to handle 1st iteration differently
        int numNodes = 0;
        while (cur = cur->next)  numNodes++;
          //  cout<<"numNodes: "<<numNodes<<", k:"<<k<<endl;
        while (numNodes >= k)
        {
            if (bDebug) cout<<"numNodes: "<<numNodes<<", k:"<<k<<endl;
            cur = prev->next; //prev always points to last node that was already reversed  
            for (int i=1; i<k; ++i)
            {
                
                ListNode* next = cur->next; // next node - reverse it to point back
               if (bDebug) printNode("set next to:",next);
                
                cur->next = next->next; // point after next so next can point back
               if (bDebug) printNode("set cur->next to:",cur->next);
                
                next->next = prev->next; // set next to point back
               if (bDebug) printNode("set next->next to:",next->next);
                
                prev->next = next; // prev next points to this iteration next (so that in next iteration new next points back to it)
               if (bDebug) printNode("set prev->next to:",prev->next);
            }
            
            prev = cur; //advance prev to last node that was already reversed  
            numNodes-=k; 
        }
        
        //delete fakeHead;
        return fakeHead->next;
        
    }
};