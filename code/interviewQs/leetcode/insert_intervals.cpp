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

void printVec( const vector<Interval>  & intervals)
{
    cout<<"[ ";

    for( auto inter : intervals)
    {
        cout<<"["<<inter.start<<", "<<inter.end<<"], ";
    }
    cout<<"]"<<endl;
}

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


    vector<Interval> insert(vector<Interval>& intervals, Interval newInterval) {
            vector<Interval> vRet;

            
            //O(NlogN)
            sort(intervals.begin(), intervals.end(), [] (const Interval & first, const Interval &second) {
                            return first.start < second.start;
                            });

            cout <<"Soreted intervals: ";
            printVec(intervals);
            //insert newInterval in place
            size_t newIntervalIndex = 0;
            for (int i=0; i<intervals.size(); ++i) //O(N)
            {
                    if (newInterval.start < intervals[i].start)
                    {
                            break;
                            //newIntervalIndex = i; //since increment on par w/ i the break value of newIntervalIndex is guaranteed to be i
                    }
                   newIntervalIndex++; 
            }

            vector<Interval>::iterator it = intervals.begin();
            intervals.insert(it+newIntervalIndex, newInterval);
            cout <<"Soreted intervals +new interval: ";
            printVec(intervals);

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


int main()
{
    vector<vector<Interval> > intervalsLists = {
            {}, {{1,3}}, {{1,3},{4,7}} , {{1,3},{2,6}}, {{10,100},{15,20}, {31,37}} , {{1,3},{2,6},{8,10},{15,18}} , {{1,4},{0,1}} ,{{4,5},{1,4},{0,1}}
    } ; 
    vector<pair<int, int>> insertMergeIntervalList = { {2,5}, {2,4} , {8,10}, {1,6}, {3,9}, {4,17}, {0,3}, {13,29} };  

    Solution sol;
    size_t idx = 0;
    for (auto intervals : intervalsLists)
    {
        cout<<"----------------------------------------------------------------------------------------------------"<<endl;
        cout<<"Inserting interval ["<<insertMergeIntervalList[0].first<<", "<<insertMergeIntervalList[0].second<<"]"<<endl;
        cout<<"Into intervals list: "<<endl;
        printVec(intervals);
        cout<<endl;

        cout<<"Inserted and Merged intervals: "<<endl;
        printVec(sol.insert( intervals ,Interval( insertMergeIntervalList[0].first, insertMergeIntervalList[0].second)) );
        cout<<"----------------------------------------------------------------------------------------------------"<<endl;
        ++idx;
    }


}
