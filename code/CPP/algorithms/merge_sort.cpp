/*
 * =====================================================================================
 *
 *       Filename:  merge_sort.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  08/16/16 21:25:20
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOSI IZAQ
 *   Organization:  
 *
 * =====================================================================================
 */
#include <iostream>
#include <vector>

using namespace std;

bool bDebug = true;
void merge(vector<int> & vec, unsigned int low, unsigned int mid, unsigned int high);

void printVec(const vector<int> & vec)
{
	cout<<"[";
	for (auto elem : vec) 
	{
		cout<<elem<<", ";

	}
	cout<<"]"<<endl;
}

void mergeSort(vector<int> & vec, unsigned int low, unsigned int high)
{

	//cout<<"mergeSort vector: "; printVec(vec);
	if (bDebug) cout<<"merge range: ["<<low<<","<<high<<"]"<<endl;
	if (low<high)
	{
		unsigned int mid = (low+high)/2;
		mergeSort(vec,low,mid);
		mergeSort(vec,mid+1,high);
		merge(vec,low,mid,high);
	}
	return;
}

void merge(vector<int> & vec, unsigned int low, unsigned int mid, unsigned int high)
{

	unsigned int i = low;
	unsigned int k = i; // for vTemp
	unsigned int j = mid+1;
	vector<int> vTemp(vec.size());

	if (bDebug) cout<<"Merge vector: "; if (bDebug) printVec(vec);
	if (bDebug) cout<<"merge range [low,mid,high]: ["<<low<<","<<mid<<","<<high<<"]"<<endl;
	while (i<=mid && j<=high) //merge until lower or upper part exhausted
	{
		if (vec[j] < vec[i])
		{
			vTemp[k++]= vec[j];
			j++;
		}
		else
		{
			vTemp[k++]= vec[i];
			i++;
		}
	}

		//finish either lower part or higher part leftover

	while (i<=mid )
	{
			vTemp[k++]= vec[i++];
	}
	while (j<=high )
	{
			vTemp[k++]= vec[j++];
	}

	if (bDebug) cout<<"Temp Merged result: "; printVec(vTemp);
	i=0;

	for(int i=low; i<k; ++i) vec[i] = vTemp[i];

	if (bDebug) cout<<"Final Merged result: "; printVec(vec);
}

int main()
{

	vector<int> vTest = {3,2,1,93,21,83,100,54};
	//vector<int> vTest = {3,2};
	mergeSort(vTest, 0, vTest.size()-1 );
	cout<<"Sorted list: "; printVec(vTest);
}

