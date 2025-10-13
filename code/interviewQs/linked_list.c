/*
 * =====================================================================================
 *
 *       Filename:  linked_list.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  04/20/15 18:48:31
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>

//single linked list
typedef struct  sll_node sll_node;
struct  sll_node //Single Linked List
{
	int val;
	sll_node * pnext;
};


int sll_insert(sll_node ** pphead, int val)
{
	printf("%s() - insert value %d \n", __func__, val);
	if (!pphead) {
	    printf("%s() - got illegal list head address \n", __func__);
	    return -1;
	}

	sll_node * ppre , *phead= NULL;
        phead = *pphead;
        printf("%s() - got list head address %p and value (head ptr) %p \n", __func__, pphead, phead);

	if ( ! phead) 
	{
	    printf("%s() - got empty head list ptr \n", __func__);
            printf("%s() - value %d will be added to a newly made list \n", __func__, val);
	    phead = malloc(sizeof(sll_node));
	    phead->val = val;
	    phead->pnext = NULL ;
	    *pphead = phead ;
	    return 0;
	}

	while (phead)
	{
		if (phead->val == val)
		{
                    printf("%s() - value %d already exists \n", __func__, val);
		    return 0;
		}
		ppre = phead ;
		phead = phead->pnext;
	}
	// here we are sure val doesnt exist and  ppre is last elem
        printf("%s() - value %d will be added to end of list \n", __func__, val);
	ppre->pnext = malloc(sizeof(sll_node));
	ppre->pnext->val = val;
	ppre->pnext->pnext = NULL;

	return 0;

}

int sll_del(sll_node ** pphead , int val)
{
	sll_node * phead = * pphead ;
	printf("%s() - delete value %d of list starting at address: %p\n", __func__, val, phead);
	if (! phead) return 0;
	if (phead->val == val)
	{
            printf("%s() - value %d will be deleted \n", __func__, val);
	    if (phead->pnext == NULL)
		{
		    free (phead);
		    phead = NULL;
		    *pphead = phead;
		}
	    else
	    {
		    sll_node * ptemp = phead;
		    phead = phead->pnext;
		    *pphead = phead;
		    free (ptemp);
		    ptemp = NULL;


	    }
		    return 0;
	}
	sll_node *pprev,*pnext = NULL;
	for (;phead->pnext != 0; phead = phead->pnext) {
		pprev = phead;
		pnext = phead->pnext;
		if (pnext->val == val)
		{
                    printf("%s() - value %d will be deleted \n", __func__, val);
		    pprev->pnext = pnext->pnext;
		    free(pnext);
		    pnext = NULL;
		    return 0;

		}
		//printf("%d%s",phead->val, (phead->pnext ? ",":""));
	}
	return 0;
}

int sll_split(sll_node * phead , int pivot, sll_node ** pLT, sll_node ** pGT)
{
	printf("%s() - split list for pivot value %d of list starting at address: %p\n", __func__, pivot, phead);
	if ( (phead == NULL) || ( phead->val == pivot) )
	{
	    printf("%s() - empty list or single element matching pivot, setting pLT to null \n", __func__);
	    *pLT = NULL;
	    *pGT = phead->pnext;
	    if (pGT)
	    {

	        printf("%s() - pGT is %d\n", __func__, (*pGT)->val);
	    }
	    else
	    {

	        printf("%s() - pGT is NULL\n", __func__);
	    }
             return 0;
	}
	for (;phead != 0; phead = phead->pnext) {
		if (phead->pnext)
		{
		    if (phead->pnext->val == pivot)
		    {
			*pLT = phead;
			if (phead->pnext)
			{
				*pGT = phead->pnext->pnext; 
			}
			else
			{
				*pGT = NULL; 
				
			}
	                printf("%s() - Pivot found, setting pLT to %d and pGT to %d%s \n", __func__, phead->val, (*pGT) ?  ( (*pGT)->val ) : -1 , (*pGT) ?  "" : "(NULL)" );
	                return 0;
		    }

		}
		else
		{
	            printf("%s() - No element matching pivot found, setting pLT and pGT to null \n", __func__);
	            *pLT = NULL;
	            *pGT = NULL;

		}
	}

	return 0;
}

int sll_print(sll_node * phead )
{
	printf("[");
	for (;phead != 0; phead = phead->pnext) {
		printf("%d%s",phead->val, (phead->pnext ? ",":""));
	}
	printf("]\n");
	return 0;
}

int srll_insert(sll_node ** pphead, int val)
{
	printf("%s() - insert value %d into sorted linked list\n", __func__, val);
	if (!pphead) {
	    printf("%s() - got illegal list head address \n", __func__);
	    return -1;
	}

	sll_node * ppre , *phead= NULL;
        phead = *pphead;
        printf("%s() - got list head address %p and value (head ptr) %p \n", __func__, pphead, phead);

	if ( ! phead) 
	{
	    printf("%s() - got empty head list ptr \n", __func__);
            printf("%s() - value %d will be added to a newly made list \n", __func__, val);
	    phead = malloc(sizeof(sll_node));
	    phead->val = val;
	    phead->pnext = NULL ;
	    *pphead = phead ;
	    return 0;
	}
	else if (phead->val > val) // Make val new head of list
	{
            printf("%s() - value %d is smaller than first element %d, making it first element... \n", __func__, val, phead->val);
	    phead = malloc(sizeof(sll_node));
	    phead->val = val;
	    phead->pnext = *pphead ;
	    *pphead = phead ;
	    return 0;

	}

	while (phead)
	{
		if (phead->val == val)
		{
                    printf("%s() - value %d already exists \n", __func__, val);
		    return 0;
		}
		ppre = phead ;
		phead = phead->pnext;
		if (phead ) 
		{
			if ( phead->val > val)
			{
				printf("%s() - value %d is smaller than element %d, putting it before it... \n", __func__, val, phead->val);
				ppre->pnext = malloc(sizeof(sll_node));
				ppre->pnext->val = val;
				ppre->pnext->pnext = phead;
				return 0;
			}
			
		}
		else //last elemet is ppre
		{
			printf("%s() - Reached end of list, value %d will be set as last element\n", __func__, val);
			ppre->pnext = malloc(sizeof(sll_node));
			ppre->pnext->val = val;
			ppre->pnext->pnext = NULL;
			return 0;
		}
	}

	return 0;

}



int sll_test()
{

	printf("Demo Single Linked List operations \n");

	sll_node * p1stlist =NULL;
	sll_node * pLT =NULL;
	sll_node * pGT =NULL;

	//Add stuff
	sll_insert(&p1stlist, 1);
	sll_insert(&p1stlist, 1);
	sll_insert(&p1stlist, 2);
	sll_insert(&p1stlist, 3);
	sll_insert(&p1stlist, 4);
	sll_insert(&p1stlist, 4);
	sll_print(p1stlist);

	sll_split(p1stlist, 2, &pLT, &pGT);
	sll_split(p1stlist, 1, &pLT, &pGT);
	sll_split(p1stlist, 4, &pLT, &pGT);

	//Delete stuff
	sll_del(&p1stlist, 3);
	sll_print(p1stlist);
	sll_del(&p1stlist, 2);
	sll_print(p1stlist);
	sll_del(&p1stlist, 1);
	sll_print(p1stlist);
	sll_del(&p1stlist, 4);
	sll_print(p1stlist);

	return 0;
}

int srll_test()
{

	printf("Demo Sorted Single Linked List operations \n");

	sll_node * p1stlist =NULL;
	sll_node * pLT =NULL;
	sll_node * pGT =NULL;

	//Add stuff
	srll_insert(&p1stlist, 5);
	srll_insert(&p1stlist, 5);
	srll_insert(&p1stlist, 2);
	srll_insert(&p1stlist, 8);
	srll_insert(&p1stlist, 4);
	srll_insert(&p1stlist, 7);
	sll_print(p1stlist);

	sll_split(p1stlist, 2, &pLT, &pGT);
	sll_split(p1stlist, 4, &pLT, &pGT);
	sll_split(p1stlist, 8, &pLT, &pGT);

	//Delete stuff
	sll_del(&p1stlist, 4);
	sll_print(p1stlist);
	sll_del(&p1stlist, 5);
	sll_print(p1stlist);
	sll_del(&p1stlist, 8);
	sll_print(p1stlist);
	sll_del(&p1stlist, 2);
	sll_print(p1stlist);

	return 0;
}
int main()
{
	printf("Demo Linked List operations \n");
	sll_test();
	srll_test();
}

