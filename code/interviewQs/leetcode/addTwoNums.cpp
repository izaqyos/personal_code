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
        
        ListNode* pCur = l1;
        long n1 = 0;
        long n2 =0;
        int tenexp=0;
        
        //cout<<"n1 "<<n1<<", n2 "<<n2<<endl;
        
        while (pCur)
        {
            n1 += (pCur->val)*pow(10,tenexp);
            //cout<<"n1 "<<n1<<", val: "<<(pCur->val)<<", multi: "<<pow(10,tenexp)<<endl;
            tenexp++;
            pCur = pCur->next;
        }
        
        ListNode* pCur2 = l2;
        tenexp=0;
        while (pCur2)
        {
            n2 += (pCur2->val)*pow(10,tenexp);
            //cout<<"n2 "<<n2<<", val: "<<(pCur2->val)<<", multi: "<<pow(10,tenexp)<<endl;
            tenexp++;
            pCur2 = pCur2->next;
        }
        
        long n3=n1+n2;
        //cout<<"n1 "<<n1<<", n2 "<<n2<<", sum:"<<n3<<endl;
        
        int leastDig = 0;
        ListNode * pRetLN = NULL;
        ListNode * pTemp = NULL;
        // i=0, dig = (n%10^(i+1))/10^i
        
        if (n3 == 0) pRetLN = new ListNode(0);
        while ((n3) > 0)
        {
            
            leastDig = n3%10;
            //cout<<"n3 "<<n3<<", least "<<leastDig<<endl;
            if (! pRetLN) 
            {
              //  cout<<"Add 1st digit "<<leastDig<<endl;
                pTemp = new ListNode(leastDig);
                pRetLN = pTemp;
            }
            else
            {
             //cout<<"Add digit "<<leastDig<<endl;
             pTemp->next  = new ListNode(leastDig);   
             pTemp = pTemp->next;
            }
            n3 /=10;
        }
       
        
        
        
        return pRetLN;
        
    }
};
