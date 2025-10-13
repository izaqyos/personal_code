/*
 * =====================================================================================
 *
 *       Filename:  binary_array_sum.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  07/01/15 10:38:07
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */

#include <stdlib.h>
#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <boost/lexical_cast.hpp>

using namespace std;
using boost::lexical_cast ;
using boost::bad_lexical_cast ;

unsigned int arrSum( vector<unsigned int> & arr, unsigned int leftI, unsigned int rightI)
{
	cout<<"calc sum for indices ("<<leftI<<","<<rightI <<")"<<endl;
	if (leftI == rightI) return arr[leftI] ;
	if (leftI < rightI) 
	{
	        cout<<"cacl sum of two subarrays, left indices ("<<leftI<<","<<((leftI+rightI)/2)<< ") right indices ("<< ((leftI + rightI)/2) +1<<","<<rightI <<")"<<endl;
		return (arrSum ( arr,leftI, (leftI+rightI)/2) +  arrSum(arr, ((leftI + rightI)/2) +1, rightI ) );
	}

	return 0;
}

int main(int argc, const char *argv[])
{

	unsigned int num = 0;
	string snum ;
	vector<unsigned int>  arr;

	while (true)
	{
	    cout<<"Plz enter numbers to be added to array. Non number to end"<<endl;
	    cin>>snum;

	    try
	    {
		num = lexical_cast<unsigned int> (snum);
		arr.push_back(num);
		//cout<<" Got number "<<num<<endl;
	    }
	    catch (bad_lexical_cast & ce)
	    {
		    cout<<"Input not number, array input is complete"<<endl;
		    cout<<"Array content: [";
		    for (vector<unsigned int>::const_iterator i = arr.begin(); i != arr.end(); ++i ) {
			if (i+1 != arr.end() ) 
			{
				cout<<(*i)<<","; 
			}
			else
			{
				cout<<(*i); 
			}
		    }
		    cout<<"]"<<endl;
		    cout<<"Array sum: "<<arrSum(arr, 0, arr.size() -1 )<<endl;
		    return 0;

	    }
	}
	return 0;
}
