/*
 * =====================================================================================
 *
 *       Filename:  KOL1502.cpp
 *
 *    Description:  
     ://www.codechef.com/problems/KOL1502>
odeChef has received a package of N ingredients from Aloo uncle and Kachori aunty as their Christmas gift. CodeChef decides to make dishes with every possible combination of these N ingredients. (Note: A dish with 0 ingredients is also possible. CodeChef uses it as an excuse for serving air to their airy customers). Every ingredient from the package has a taste score between 1 and 10.
Now CodeChef has customers on two planets, planet A and planet B. People from planet A like all the ingredients very much. And hence for every dish given to them, planet A will pay CodeChef an amount, which, in Alterian dollars, equals the sum of the taste scores of all the ingredients present in the dish minus the sum of the taste scores of all the ingredients not present in the dish.
People from planet B don't like the ingredients at all. So for every dish given to planet B, planet B will pay CodeChef Alterian dollars equal to the sum of the taste scores of all the ingredients not present in the dish minus the sum of the taste scores of all the ingredients present in the dish.
CodeChef can only make a single dish from a particular combination of ingredients. And they can send a dish either to planet A or planet B, but not both. You have to find out the maximum amount of money CodeChef will make by distributing all the dishes made with these ingredients on planet A and planet B.
Report the maximum amount modulo 107.
Input

The first line contains T, the number of test cases.
Each test case begins with N, the number of ingredients
The next line for the test case contains N space-separated integers, which are the taste scores of the ingredients.
Output

For each test case, output the value as asked in a separate line.
Constraints

1 ≤ T ≤ 100
1 ≤ N ≤ 1000
1 ≤ Taste scores of ingredients ≤ 10
1 ≤ Sum of N over all Test Cases ≤ 1000
Example

Input:
1
2
1 2
Output:
8
Explanation

Example case 1. The dishes made by CodeChef and the amounts collected:
Dish 1: Contains both ingredients: Sold to Planet A for 3 Alterian dollars.
Dish 2: Contains first ingredients: Sold to Planet B for 1 Alterian dollars.
Dish 3: Contains second ingredients: Sold to Planet A for 1 Alterian dollars.
Dish 4: Does not contain any ingredients: Sold to Planet B for 3 Alterian dollars.
Total Amount : 8 Alterian dollars.
 *
 *        Version:  1.0
 *        Created:  03/24/16 17:17:47
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Yosi Izaq
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <set>
#include <vector>
#include <algorithm> //std::find
#include<cstdlib> //rand srand
#include<ctime> // time
#include <boost/algorithm/string/split.hpp> 
#include <boost/algorithm/string/classification.hpp> 

using namespace std;

void add_elem_2_sets(int elem, set<set<int> > & ret_set) 
{
	for (set<set<int> >::iterator it = ret_set.begin(); it != ret_set.end(); ++it )
	{
		set<int>  curr_set  (*it);
		curr_set.insert(elem);
		ret_set.erase(it);
		ret_set.insert(curr_set);
	}
}

void unite_sets_of_sets(const set< set<int> >  & set1,const set< set<int> >  & set2,  set<set<int> > & ret_set) 
{
	ret_set.clear();
	for (set<set<int> >::const_iterator cit = set1.begin(); cit != set1.end() ; ++cit)
	{
		ret_set.insert(*cit);
	}
	for (set<set<int> >::const_iterator cit = set2.begin(); cit != set2.end(); ++cit )
	{
		ret_set.insert(*cit);
	}
}

void ret_subset(const  vector<unsigned int>& num_list, set<set<int> > & ret_set )
{
		//cout<<"ret_subset called \n";
	set<set<int> >  setswith1stelem;
	set<set<int> >  setswithout1stelem;
	ret_set.clear();
	set<int> empty_set;
	vector<unsigned int> num_list_copy (num_list);
	if (num_list_copy.empty()) 
	{
		//cout<<"adding empty set\n";
		ret_set.insert(empty_set);
	}
	else
	{
		//cout<<"adding sub sets\n";
		int elem = num_list[0];
		num_list_copy.erase(num_list_copy.begin());

		ret_subset(num_list_copy, setswith1stelem);
		add_elem_2_sets(elem, setswith1stelem ); // all sets w/ elem	

		ret_subset(num_list_copy, setswithout1stelem); // all sets w/o elem	
		unite_sets_of_sets(setswith1stelem, setswithout1stelem, ret_set);
	}

}
void print_set( const set<int> & myset)
{
	cout<<"{ ";
	for (set<int>::const_iterator cit = myset.begin(); cit != myset.end(); ++cit )
	{
		cout<<*cit<<", ";
	}
	cout<<"}\n";
}

void print_setofsets( const set< set<int> > & myset)
{
	cout<<"{\n";
	for (set< set<int> >::const_iterator cit = myset.begin(); cit != myset.end(); ++cit )
	{
		print_set(*cit);
	}
	cout<<"}\n";
}

class ChefTester
{
	public:
	ChefTester();
	ChefTester( const unsigned int numTests, const unsigned int numIngredients, const vector<unsigned int> & vecIngredients);
	~ChefTester();

	void runTests() const;
	void printMe() const;

	protected:
	private:
	
	unsigned int serveToA(const set<int> & dish) const;
	unsigned int serveToB(const set<int> & dish) const;
	unsigned int m_numTests;
	unsigned int m_numIngredients;
	vector<unsigned int> m_vecIngredients;
};

ChefTester::~ChefTester()
{
	m_vecIngredients.clear();

}

ChefTester::ChefTester():
	m_numTests(0),
	m_numIngredients(0),
	m_vecIngredients()
{

}

ChefTester::ChefTester( const unsigned int numTests, const unsigned int numIngredients, const vector<unsigned int> & vecIngredients):
	m_numTests(numTests),
	m_numIngredients(numIngredients),
	m_vecIngredients(vecIngredients)
{

}

void ChefTester::printMe() const
{
	cout<<"ChefTester data:\n";
	cout<<"{numTests="<<m_numTests<<", numIngredients="<<m_numIngredients<<" }\n";
	cout<<"Ingredients: ";
	for (vector<unsigned int>::const_iterator it = m_vecIngredients.begin(); it != m_vecIngredients.end() ; ++it)
	{
		cout<<*it<<", ";
	}
	cout<<"\n";
}

unsigned int ChefTester::serveToA(const set<int> & dish) const
{

	unsigned int payment  = 0;
	set<int> notInDish;
	set<int>::iterator sit;
	vector<unsigned int>::iterator vit;

		//Calculate ingredients not in dish
	for (vector<unsigned int>::const_iterator it = m_vecIngredients.begin(); it != m_vecIngredients.end() ; ++it)
	{
		if (dish.find(*it) == dish.end() ) // This ingredient is not in dish
		{
			//cout<<"ChefTester::serveToA() - adding ingredient "<<*it<<" to notInDish\n";
			notInDish.insert(*it);
		}
	}

		//Calculate payment for ingredients in dish
	for (set<int>::const_iterator cit = dish.begin(); cit != dish.end(); ++cit )
	{
		payment+=(*cit);
		//cout<<"ChefTester::serveToA() - adding ingredient in dish"<<*cit<<" payment. Total payment: "<<payment<<"\n";
	}

		//Calculate payment for ingredients not in dish
	for (set<int>::const_iterator cit = notInDish.begin(); cit != notInDish.end(); ++cit )
	{
		if ( payment >= (*cit) ) 
		{
			payment-=(*cit); // prevent underflow
		}
		else
		{
			payment=0;
		}
		//cout<<"ChefTester::serveToA() - substracting ingredient not in dish"<<*cit<<" payment. Total payment: "<<payment<<"\n";
	}

	//cout<<"ChefTester::serveToA() - Total payment: "<<payment<<"\n";
	return payment;
}

unsigned int ChefTester::serveToB(const set<int> & dish) const
{

	unsigned int payment  = 0;
	set<int> notInDish;
	set<int>::iterator sit;
	vector<unsigned int>::iterator vit;

		//Calculate ingredients not in dish
	for (vector<unsigned int>::const_iterator it = m_vecIngredients.begin(); it != m_vecIngredients.end() ; ++it)
	{
		if (dish.find(*it) == dish.end() ) // This ingredient is not in dish
		{
			//cout<<"ChefTester::serveToB() - adding ingredient "<<*it<<" to notInDish\n";
			notInDish.insert(*it);
		}
	}

		//Calculate payment for ingredients not in dish
	for (set<int>::const_iterator cit = notInDish.begin(); cit != notInDish.end(); ++cit )
	{
		payment+=(*cit);
		//cout<<"ChefTester::serveToB() - adding ingredient not in dish"<<*cit<<" payment. Total payment: "<<payment<<"\n";
	}
	
		//Calculate payment for ingredients in dish
	for (set<int>::const_iterator cit = dish.begin(); cit != dish.end(); ++cit )
	{
		if ( payment >= (*cit) ) 
		{
			payment-=(*cit); // prevent underflow
		}
		else
		{
			payment=0;
		}
		//cout<<"ChefTester::serveToB() - substracting ingredient in dish"<<*cit<<" payment. Total payment: "<<payment<<"\n";
	}

	//cout<<"ChefTester::serveToA() - Total payment: "<<payment<<"\n";
	return payment;

}

void ChefTester::runTests() const
{
	//cout<<"ChefTester::runTests()\n";

	//cout<<"ChefTester::runTests() - Calculating dishes...\n";
	set<set<int> > dishes;
	ret_subset(m_vecIngredients, dishes);

	srand(time(NULL));

	unsigned int score  = 0;
	for (unsigned int i = 0; i < m_numTests; i++) 
	{
	//	cout<<"ChefTester::runTests() - Running test "<<i<<" ...\n";
		for (set<set<int> >::const_iterator cit = dishes.begin(); cit != dishes.end() ; ++cit)
		{
			//cout<<"Serving dish:\n";
			//print_set(*cit);
			if (rand() % 2) 
			{
			//	cout<<"To customer A\n";
				score += serveToA(*cit);

			}
			else
			{
			//	cout<<"To customer B\n";
				score += serveToB(*cit);
			}
		}
		//cout<<"ChefTester::runTests() - Score for test "<<i<<" is: "<<score<<"\n";
		cout<<score<<"\n";

	}
}

int main()
{

	/* *
	set<set<int> > superset, test_superset;
	set<int> test_set, test_set1;

	vector<unsigned int> num_list;

	for (int i=0; i<5; ++i) 
	{
		test_set.insert(i);
		num_list.push_back(i);
	}

	for (int i=3; i<9; ++i) 
	{
		test_set1.insert(i);
	}

	cout<<"Test sets:\n";
	print_set(test_set);
	print_set(test_set1);
	test_superset.insert(test_set);
	test_superset.insert(test_set1);
	add_elem_2_sets(10, test_superset); 

	cout<<"Unite sets and add element 10 to each:\n";
	print_setofsets(test_superset);

	cout<<"Print superset of first list:\n";
	ret_subset(num_list, superset);
	print_setofsets(superset);
	*/


	//cout<<"Starting dish tests:\n";
	unsigned int numTests = 0;
	unsigned int numIngredients = 0;
	unsigned int ingredient = 0;
	vector<unsigned int> vecIngredients;

	//cout<<"Enter number of tests:\n";
	//cin>>numTests;
	//cout<<"Enter number of ingredients:\n";
	//cin>>numIngredients;
	//for (unsigned int i = 0; i < numIngredients; i++) {
	//	cout<<"Enter ingredient number "<<i<<" :\n";
	//	cin>>ingredient;

	//	vecIngredients.push_back(ingredient);
	//}
	string sLine;
	vector<string> vecstrIng;
	for (int i = 0; i < 3; i++) {
		getline(cin, sLine);
		if (i == 0 ) { numTests = stoi(sLine, nullptr);}
		if (i == 1 ) { numIngredients = stoi(sLine, nullptr);}
		if (i == 2 ) 
		{ 
			boost::algorithm::split(vecstrIng, sLine, boost::is_any_of(" ")) ;	
			for (vector<string>::iterator vit = vecstrIng.begin() ; vit != vecstrIng.end() ; ++vit)
			{
				vecIngredients.push_back(stoi(*vit, nullptr));
			}
		}
	}

	ChefTester ct(numTests, numIngredients, vecIngredients);
	//ct.printMe();
	ct.runTests();

}


/* *
 *
 Run example for submission:
[yizaq@YIZAQ-M-D1BW:Tue Apr 05:~/Desktop/Work/code/CPP/practice:]$ g++ KOL1502.cpp -I /usr/local/Cellar/boost/1.55.0/include/  -o KOL1502
[yizaq@YIZAQ-M-D1BW:Tue Apr 05:~/Desktop/Work/code/CPP/practice:]$ ./KOL1502 
1
2
1 2
5
 Run example w/ all prints enabled:

[yizaq@YIZAQ-M-D1BW:Mon Apr 04:~/Desktop/Work/code/CPP/practice:]$ g++ KOL1502.cpp  -o KOL1502
[yizaq@YIZAQ-M-D1BW:Mon Apr 04:~/Desktop/Work/code/CPP/practice:]$ ./KOL1502 
Test sets:
{ 0, 1, 2, 3, 4, }
{ 3, 4, 5, 6, 7, 8, }
Unite sets and add element 10 to each:
{
{ 0, 1, 2, 3, 4, 10, }
{ 3, 4, 5, 6, 7, 8, 10, }
}
Print superset of first list:
{
{ }
{ 0, }
{ 0, 1, }
{ 0, 1, 2, }
{ 0, 1, 2, 3, }
{ 0, 1, 2, 3, 4, }
{ 0, 1, 2, 4, }
{ 0, 1, 3, }
{ 0, 1, 3, 4, }
{ 0, 1, 4, }
{ 0, 2, }
{ 0, 2, 3, }
{ 0, 2, 3, 4, }
{ 0, 2, 4, }
{ 0, 3, }
{ 0, 3, 4, }
{ 0, 4, }
{ 1, }
{ 1, 2, }
{ 1, 2, 3, }
{ 1, 2, 3, 4, }
{ 1, 2, 4, }
{ 1, 3, }
{ 1, 3, 4, }
{ 1, 4, }
{ 2, }
{ 2, 3, }
{ 2, 3, 4, }
{ 2, 4, }
{ 3, }
{ 3, 4, }
{ 4, }
}
Starting dish tests:
Enter number of tests:
1
Enter number of ingredients:
2
Enter ingredient number 0 :
1
Enter ingredient number 1 :
2
ChefTester data:
{numTests=1, numIngredients=2 }
Ingredients: 1, 2, 
ChefTester::runTests()
ChefTester::runTests() - Calculating dishes...
ChefTester::runTests() - Running test 0 ...
Serving dish:
{ }
To customer B
ChefTester::serveToB() - adding ingredient 1 to notInDish
ChefTester::serveToB() - adding ingredient 2 to notInDish
ChefTester::serveToB() - adding ingredient not in dish1 payment. Total payment: 1
ChefTester::serveToB() - adding ingredient not in dish2 payment. Total payment: 3
ChefTester::serveToA() - Total payment: 3
Serving dish:
{ 1, }
To customer B
ChefTester::serveToB() - adding ingredient 2 to notInDish
ChefTester::serveToB() - adding ingredient not in dish2 payment. Total payment: 2
ChefTester::serveToB() - substracting ingredient in dish1 payment. Total payment: 1
ChefTester::serveToA() - Total payment: 1
Serving dish:
{ 1, 2, }
To customer B
ChefTester::serveToB() - substracting ingredient in dish1 payment. Total payment: 0
ChefTester::serveToB() - substracting ingredient in dish2 payment. Total payment: 0
ChefTester::serveToA() - Total payment: 0
Serving dish:
{ 2, }
To customer A
ChefTester::serveToA() - adding ingredient 1 to notInDish
ChefTester::serveToA() - adding ingredient in dish2 payment. Total payment: 2
ChefTester::serveToA() - substracting ingredient not in dish1 payment. Total payment: 1
ChefTester::serveToA() - Total payment: 1
ChefTester::runTests() - Score for test 0 is: 5
 * */
