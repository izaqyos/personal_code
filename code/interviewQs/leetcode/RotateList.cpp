//build: clang++ -Wc++17-extensions -std=c++17 RotateList.cpp
#include <iostream>
#include <vector>
#include <algorithm> 
#include <iterator> 
#include <numeric> //iota

using namespace std;

 struct ListNode {
     int val;
     ListNode *next;
     ListNode(int x) : val(x), next(NULL) {}
 };

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */

//class LinkedList{
//        
//
//};

class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
            if (!head || ! head->next ) return head;

            ListNode* runner = head;
            ListNode* tail = head;
            unsigned int size = 0;

            while(runner) {
                    runner = runner->next;
                    size++;
            }
            tail=runner;
            k%=size;

            if (k==0) return head;

            runner = head;
            for (int i=0; i< size-k-1; ++i){
                    runner = runner->next;
            }
            tail->next = head;
            head = runner->next;
            runner->next=nullptr;

            return head;
}

    void printList(ListNode* head)
    {
            if (! head ) return ;
            while (head)
            {
                    cout<<head->val<<"->";
                    head = head->next;
            }
            cout<<"||-"<<endl;
    }

    void printVector(vector<int> & vec){
            cout<<"printVector()"<<endl;
            cout<<"<";
            for (auto elem  : vec){
                    cout<<elem<<",";
            }
            //std::copy(vec.begin(), vec.end(), std::ostream_iterator<int>(std::cout, ""));
            cout<<">";
            cout<<endl;
    }

    static ListNode* listify(vector<int> & list)
    {
            ListNode* head = nullptr;
            ListNode* tmp;
            for (auto n : list)
            {
                    tmp = new ListNode(n);
                    if (head == nullptr) head=tmp;
                    else head->next = tmp;
            }

            return head;
    }

    static void deleteList(ListNode * head)
    {
            ListNode *tmp  = head;
            while(head)
            {
                    head = head->next;
                    delete tmp;
                    tmp = head;
            }
    }
    
};

int main()
{

        cout<<"Testing rotateList"<<endl;
        ListNode *headNode = (ListNode *)new ListNode(0);
        ListNode *tailNode = (ListNode *)new ListNode(1);
        headNode->next=tailNode;
        cout<<"Created list "<<headNode->val<<"->"<<tailNode->val<<endl;

        Solution sol ;
        sol.printList(headNode);
        Solution::deleteList(headNode);

        cout<<"Creating empty Vector "<<endl;
        vector<vector<int> > listOfLists;
        vector<int> emptyV;
        listOfLists.push_back(emptyV);
        
        cout<<"Creating Vector with one element"<<endl;
        vector<int> range1V(1,0);
        listOfLists.push_back(range1V);

        cout<<"Creating Vector with two element"<<endl;
        vector<int> range2V(2);
        iota(range2V.begin(), range2V.end(), 0);
        listOfLists.push_back(range2V);

        cout<<"Creating Vector with three element"<<endl;
        vector<int> range3V(3);
        iota(range3V.begin(), range3V.end(), 0);
        listOfLists.push_back(range3V);

        cout<<"Creating Vector with four element"<<endl;
        vector<int> range4V(4);
        iota(range4V.begin(), range4V.end(), 0);
        listOfLists.push_back(range4V);

        cout<<"Creating Vector with 100 element"<<endl;
        vector<int> range100V(100);
        iota(range4V.begin(), range100V.end(), 0);
        listOfLists.push_back(range100V);

        cout<<"processing lists"<<endl; 
        for (vector<vector<int>>::const_iterator ci = listOfLists.begin() ; ci != listOfLists.end() ; ++ci){
                cout<<"Processing vector:";
              sol.printVector((vector<int> &    )*ci);
        }
        //for (auto v : listOfLists)
        //{
        //        cout<<"Processing vector:";
        //        //sol.printVector(v);
        //        //ListNode *head = sol.listify(v);
        //        //cout<<"Rotating list: ";
        //        //sol.printList(head);
        //        //for (auto n : v)
        //        //{
        //        //    cout<<"Rotating list: "<<n<<", ";
        //        //}
        //        //cout<<"}"<<endl;
        //}
}
