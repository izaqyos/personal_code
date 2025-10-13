#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <algorithm>
#include <iterator>

using namespace std;

void printSet(const unordered_set<int> & set)
{
    
        cout<<"{ ";
    std::copy(set.begin(), set.end(), ostream_iterator<int>(cout,", "));
        cout<<"} ";
    //cout<<endl;
}

void printSuperSet(const vector<unordered_set<int>> & sets)
{
        cout<<"{ ";
        for (auto set : sets) 
        {
                printSet(set);
        }
        cout<<"} ";
}

vector<unordered_set<int>> superset(const unordered_set<int> & set)
{
        vector<unordered_set<int>> sets;
        vector<unordered_set<int>> tempsets;
        unordered_set<int> tset;
        sets.insert(tset);

        for (auto n : set)
        {
                //each element is either in all the subsets of set sans itself
                // or it is not. 
                // ex. {1,2,3} -> 1 is either in {2,3} subset ({1},{1,2},{1,3},{1,2,3)
                // or not ({},{2},{3},{2,3)

                tempset = superset(set.erase(n) );
                for (auto iset : tempset)
                {
                        sets.insert(iset);
                        sets.insert(iset.insert(n));

                }
        }

        return sets;
}





int main()
{
        vector<unordered_set<int>> inpSet={ 
                {},
                {1},
                {1,2},
                {1,2,3},
                {1,2,3,4,5,6,7,8,9},
        };

        vector<unordered_set<int>> sets;
        for (auto set : inpSet)
        {
                cout<<"Calculating super set of set:"<<endl;
                printSet(set);
                sets = superset(set);
                printSuperSet(sets);



        }
}
