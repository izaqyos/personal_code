/**
Given a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list.

Return the linked list sorted as well.

Example 1:

Input: 1->2->3->3->4->4->5
Output: 1->2->5
Example 2:

Input: 1->1->1->2->3
Output: 2->3
**/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        /*
        idea, 
        1st step remove leading sames, move header to 1st elem post sames
        2nd step. there r two distinct elements. use 2 ptrs. prev, curr
        for curr run loop to delete if there r sames.
        if not prev,curr = curr, curr->next
        */

        ListNode* prev;
        ListNode* curr;
        
        //process prefix of sames
        // exit cond. a. curr is null (finished list), b. prev != curr
        while (true) { 
            if ( (head == nullptr) || (head->next == nullptr) ) return head;
            prev = head;
            curr = head->next;
            
            if ( (curr != nullptr) && (curr->val  == prev->val ) ) {
                curr = curr->next;
                while ((curr != nullptr) && (curr->val == prev->val)) {
                    curr = curr->next; 
                }
                head = curr;
            }
            else {
                break;
            }
        }

        if (curr == nullptr) return head;
        //maintain invarianta: prev and curr are distinct.
        while (curr->next != nullptr) {
            if (curr->next->val == curr->val) {
                while (( curr->next != nullptr) && (curr->next->val == curr->val)) {
                    curr = curr->next;
                } 
                prev->next = curr;
            }
            else {
                prev = curr;
                curr = curr->next;
            } 
        }

        return head;
    }
};