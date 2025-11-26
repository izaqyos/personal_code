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
struct comp{
    bool operator ()(const pair<ListNode* , int> & a, const pair<ListNode* , int> & b )
    {
        return b.second < a.second;
    }
};

    ListNode* mergeKLists(vector<ListNode*>& lists) {
        
        vector< pair<ListNode* , int>> minHeap;
        make_heap(minHeap.begin(), minHeap.end(), comp());
        ListNode* head = nullptr;
        ListNode* last = nullptr;

        vector<ListNode*> listCpy = lists;        
        while (!lists.empty())
        {
            for (int i=0; i<lists.size(); i++)
            {
                if (lists[i])
                {
                    minHeap.push_back(make_pair(lists[i], lists[i]->val));
                    push_heap(minHeap.begin(), minHeap.end(),comp());
                    lists[i] = lists[i]->next;
                }
                else
                {
                    lists.erase(lists.begin()+i); // delete empty lists
                }
            }
        }
        // now lists empty. minHeap contains all values.
        
        lists = listCpy;
        //build new sorted list
            //push min to new list
            pair<ListNode* , int> minPair;
        while (!minHeap.empty())
        {
            
             minPair = minHeap.front();
            pop_heap(minHeap.begin(), minHeap.end(),comp());
            minHeap.pop_back();
            //cout<<" poped: "<<minPair.second<<endl;
            if (head)
                    {
                        //cout<<"Add head->next: "<<minPair.second<<endl;
                        last->next = minPair.first;
                        last = last->next;
                    }
                    else
                    {
                       // cout<<"Add head: "<<minPair.second<<endl;
                        head = minPair.first; //start new list
                        last = head;
                    }
                   
        }
        
        return head;
        
    }
};