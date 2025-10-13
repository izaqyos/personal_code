#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>

using namespace std;

/**
 * Definition for an interval.
 * struct Interval {
 *     int start;
 *     int end;
 *     Interval() : start(0), end(0) {}
 *     Interval(int s, int e) : start(s), end(e) {}
 * };
 */

struct Interval {
     int start;
     int end;
     Interval() : start(0), end(0) {}
     Interval(int s, int e) : start(s), end(e) {}
 };

class Solution {
public:
    vector<Interval> merge(vector<Interval>& intervals) {
            vector<Interval> vRet;

            if (intervals.empty()) return vRet;
            sort(intervals.begin(), intervals.end(), [] (const Interval & first, const Interval &second) {
                            return first.start < second.start;
                            });

            bool bOverlap = false;
            Interval overlap;

            for (int i=0; i< intervals.size()-1; ++i) // note, loop ends on 2nd from last element
            {
                if (bOverlap)
                {
                    if (overlap.end >= intervals[i+1].start)
                    {
                            overlap.end = max(overlap.end, intervals[i+1].end);
                    }
                    else
                    {
                        vRet.push_back(overlap);
                        bOverlap = false;
                    }
                }
                else
                {
                    if (intervals[i].end >= intervals[i+1].start)
                    {
                        bOverlap = true;
                        overlap.start = intervals[i].start;
                        overlap.end = max(intervals[i].end, intervals[i+1].end);
                        bOverlap = true;
                    }
                    else
                    {
                        overlap.start = intervals[i].start;
                        overlap.end = intervals[i].end;
                        vRet.push_back(overlap);
                    }
                }

            } // for

            //handle last indice, if needed
            if (bOverlap)
            {
                vRet.push_back(overlap);
            }
            else
            {
                vRet.push_back(Interval(intervals[intervals.size()-1].start, intervals[intervals.size()-1].end) );
            }
            
            return vRet;
        
    }
};

void printVec( const vector<Interval>  & intervals)
{
    cout<<"[ ";

    for( auto inter : intervals)
    {
        cout<<"["<<inter.start<<", "<<inter.end<<"], "<<endl;
    }
    cout<<"]";
}

int main()
{
    vector<vector<Interval> > intervalsLists = {
            {}, {{1,3}}, {{1,3},{4,7}} , {{1,3},{2,6}}, {{10,100},{15,20}, {31,37}} , {{1,3},{2,6},{8,10},{15,18}} , {{1,4},{0,1}} ,{{4,5},{1,4},{0,1}}
    } ; 
    Solution sol;
    for (auto intervals : intervalsLists)
    {
        cout<<"Merging intervals of intervals list: "<<endl;
        printVec(intervals);
        cout<<endl;

        cout<<"Merged intervals: "<<endl;
        printVec(sol.merge(intervals));
        cout<<endl;
    }


}
