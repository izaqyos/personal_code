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
    ListNode* swapPairs(ListNode* head) {
     
     if ((head == nullptr) || (head->next == nullptr))   return head;
     
     ListNode * pCur = head;
     ListNode * pPrev = head;
     ListNode *pTmp = nullptr;
     
     while ((pCur != nullptr) && (pCur->next != nullptr))
     {
         pTmp = pCur->next;
         pCur->next = pTmp->next; 
         pTmp->next = pCur;
         if (pCur == head) head = pTmp;
         else pPrev->next = pTmp;
         
         pPrev = pCur;
         pCur = pPrev->next;
     }
     
     return head;
    }
};