/**
 * Definition for an interval.
 * struct Interval {
 *     int start;
 *     int end;
 *     Interval() : start(0), end(0) {}
 *     Interval(int s, int e) : start(s), end(e) {}
 * };
 */
class Solution {
public:
    vector<Interval> insert(vector<Interval>& intervals, Interval newInterval) {
                    vector<Interval> vRet;

            
            //O(NlogN)
            sort(intervals.begin(), intervals.end(), [] (const Interval & first, const Interval &second) {
                            return first.start < second.start;
                            });

            //cout <<"Soreted intervals: ";
            //printVec(intervals);
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
            //cout <<"Soreted intervals +new interval: ";
            //printVec(intervals);

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