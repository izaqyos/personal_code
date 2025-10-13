#!/usr/bin/python
#Definition for an interval.
class Interval(object):
    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e

    def __repr__(self):
        return '[{0},{1}]'.format(self.start, self.end)

def getKey(interval):
    return interval.start

class Solution(object):
    bDebug = True

    def merge(self, intervals):
        """
        :type intervals: List[Interval]
        :rtype: List[Interval]
        """

        retIntervals = list()
        #first, sort by start
        sortedIntervals = sorted(intervals, key=getKey)
        overlapFound = False 
        overlap = Interval()

        if Solution.bDebug: print "Merging intervals list {0}".format(intervals) 
        if Solution.bDebug: print "Sorted intervals list {0}".format(sortedIntervals)
        for i,interval in enumerate(sortedIntervals):
            if Solution.bDebug: print "Processing interval {0}, val: {1}".format(i,interval)
            if i == (len(intervals)-1):
                continue

            if overlapFound:
                if Solution.bDebug: print "Scanning state: overlapFound"
                if overlap.end >= sortedIntervals[i+1].start: #nice lets add to interval
                    overlap.end = max(overlap.end, sortedIntervals[i+1].end)
                else:
                    retIntervals.append(overlap)
                    overlapFound = False

            else:
                if Solution.bDebug: print "Scanning state: no overlapFound. compare this intervals end ({0}) with next start {1}".format(interval.end , intervals[i+1].start)
                if interval.end >= sortedIntervals[i+1].start: #nice lets start recording an overlap
                    overlap = Interval(interval.start, max(interval.end, sortedIntervals[i+1].end))
                    overlapFound = True
                else: #no overlap, add to ret list
                    retIntervals.append(interval)

        #add overlap if needed, else add last
        if overlapFound:
            retIntervals.append(overlap)
        elif len(sortedIntervals) > 0:
            retIntervals.append(sortedIntervals[len(sortedIntervals)-1])


        return retIntervals

    def insert(self, intervals, newInterval):
        """
        :type intervals: List[Interval]
        :type newInterval: Interval
        :rtype: List[Interval]
        """
        retIntervals = list()
        #first, sort by start, O(NlogN)
        sortedIntervals = sorted(intervals, key=getKey)

        #now, insert newInterval in place O(N)
        bIsInserted = False
        lenSortedIntervalsList = len(sortedIntervals)
        for i in range(lenSortedIntervalsList): #I know xrange is better, but in 3.0 its gone and range works as generator...
            if (sortedIntervals[i].start > newInterval.start):
                print "Attempt to insert interval {0} at index {1} of list {2}".format(newInterval, i, sortedIntervals)
                sortedIntervals.insert(i, newInterval)
                bIsInserted = True

        #if newInterval.start > all sortedIntervals[i].start ...
        if (not bIsInserted):
            sortedIntervals.insert(len(sortedIntervals), newInterval)



        overlapFound = False 
        overlap = Interval()

        if Solution.bDebug: print "Merging intervals list {0}".format(intervals) 
        if Solution.bDebug: print "Sorted intervals list {0}".format(sortedIntervals)


        for i,interval in enumerate(sortedIntervals):
            if Solution.bDebug: print "Processing interval {0}, val: {1}".format(i,interval)
            if i == (len(sortedIntervals)-1):
                continue

            if overlapFound:
                if Solution.bDebug: print "Scanning state: overlapFound"
                if overlap.end >= sortedIntervals[i+1].start: #nice lets add to interval
                    overlap.end = max(overlap.end, sortedIntervals[i+1].end)
                else:
                    retIntervals.append(overlap)
                    overlapFound = False

            else:
                if Solution.bDebug: print "Scanning state: no overlapFound. compare this intervals end ({0}) with next start {1}".format(interval.end , sortedIntervals[i+1].start)
                if interval.end >= sortedIntervals[i+1].start: #nice lets start recording an overlap
                    overlap = Interval(interval.start, max(interval.end, sortedIntervals[i+1].end))
                    overlapFound = True
                else: #no overlap, add to ret list
                    retIntervals.append(interval)

        #add overlap if needed, else add last
        if overlapFound:
            retIntervals.append(overlap)
        elif len(sortedIntervals) > 0:
            retIntervals.append(sortedIntervals[len(sortedIntervals)-1])


        return retIntervals


def makeIntervalsFromPairsList(pairList):
    intervalsList = list()
    for p in pairList:
        intervalsList.append(Interval(p[0],p[1]))
    return intervalsList


def main():
    intervalsLists = [ [], [[1,3]], [[1,3],[4,7]] , [[1,3],[2,6]], [[10,100],[15,20], [31,37]] , [[1,3],[2,6],[8,10],[15,18]] , [[1,4],[0,1]] ,[[4,5],[1,4],[0,1]]]
    insertMergeIntervalList= [ [2,5], [2,4] , [8,10], [1,6], [3,9], [4,17], [0,3], [13,29] ] 
    #intervalsLists = [[[1,4],[0,1]] ]
    #intervalsLists = [ [[4,5],[1,4],[0,1]]  ]
    sol = Solution()
    for i,l in enumerate(intervalsLists):
        print "intervals[{1}]: {0}".format(l, i)
        newInterval = Interval(insertMergeIntervalList[i][0], insertMergeIntervalList[i][1])
        print "new intreval to insert {0}".format(newInterval)
        #print "new intreval to insert {0}".format(insertMergeIntervalList[i])
        mergedList = sol.insert( makeIntervalsFromPairsList(l), newInterval)
        print "merged intervals: {0}".format(mergedList)
        print '-'*120

if __name__ == "__main__":
    main()

