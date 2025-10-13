//Definition for singly-linked list.
struct ListNode {
   int val;
   ListNode *next;
   ListNode() : val(0), next(nullptr) {}
   ListNode(int x) : val(x), next(nullptr) {}
   ListNode(int x, ListNode *next) : val(x), next(next) {}
};


	class Solution {
	public:
		//Finding the Middle element and divide into two lists
		void divideIntoHalve(ListNode* head, ListNode** l1, ListNode** l2)
		{
			ListNode* slowptr = head;
			ListNode* fastptr = head->next;
			while(fastptr && fastptr->next)
			{
				slowptr = slowptr->next;
				fastptr = fastptr->next->next;
			}
			*l1 = head;
			*l2 = slowptr->next;
			slowptr->next = nullptr;

		}
	//Merging the two lists
	ListNode* merge(ListNode* l1, ListNode* l2)
	{
		//head is for soring the sorted list of l1 and l2 and temp will pont to last minimum node which is added 
		//into sorted list from l1 or l2
		ListNode* head = nullptr, *temp;
		while(l1 and l2)
		{
			if(l1->val <= l2->val)
			{
				if(head == nullptr)
				{
					head = l1;
					temp = head;
					l1 = l1->next;
					temp->next = nullptr;
				}else{
					temp->next = l1;
					temp = temp->next;
					l1 = l1->next;
					temp->next = nullptr;
				}
			}
			else{

				if(head == nullptr)
				{
					head = l2;
					temp = head;
					l2 = l2->next;
					temp->next = nullptr;
				}
				else{
					temp->next = l2;
					temp = temp->next;
					l2 = l2->next;
					temp->next = nullptr;
				}
			}
		}
		//This loops are to add remaining elements into sorted list(head)
		while(l1){
			temp->next = l1;
			temp = temp->next;
			l1 = l1->next;
			temp->next = nullptr;
		}
		while(l2)
		{
			temp->next = l2;
			temp = temp->next;
			l2 = l2->next;
			temp->next = nullptr;
		}
		return head;
	}
	void mergeSort1(ListNode** head)
	{
			if(!(*head) or !(*head)->next)
				return;
			ListNode *l1, *l2;
			divideIntoHalve(*head, &l1, &l2);
			mergeSort1(&l1);
			mergeSort1(&l2);
			l1 = merge(l1, l2);
			//head is to hold and update the sorted list
			*head = l1;
	}
	ListNode* sortList(ListNode* head) {
			mergeSort1(&head);
			return head;
		}
};
