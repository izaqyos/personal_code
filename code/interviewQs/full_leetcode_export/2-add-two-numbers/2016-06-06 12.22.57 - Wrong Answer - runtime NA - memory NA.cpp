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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        int n1= l1->val;
        if (l1->next)
        {
            n1+= (( l1->next->val)*10);
            if (l1->next->next)  n1+= (( l1->next->next->val)*100);
        }
       
        
        
        int n2= l2->val;
        if (l2->next)
        {
            n2+= (( l2->next->val)*10);
            if (l2->next->next)  n2+= (( l2->next->next->val)*100);
        }
        
        
        int n3=n1+n2;
        
       
        int n3h = n3/100;
        int n3m = (n3%100)/10;
        int n3l = (n3%100)%10;
         
        //cout<<"n1: "<<n1<<", n2: "<<n2<<", sum: "<<n3<<endl;
        ListNode * pRetLN = new ListNode(n3l);
        if (n3>9)
        {
            pRetLN->next = new ListNode(n3m);
            if (n3>99) pRetLN->next->next = new ListNode(n3h);
        }
        
        
        return pRetLN;
        
    }
};