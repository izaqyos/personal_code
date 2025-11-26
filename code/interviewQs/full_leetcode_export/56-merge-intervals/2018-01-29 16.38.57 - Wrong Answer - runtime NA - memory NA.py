# Definition for an interval.
# class Interval(object):
#     def __init__(self, s=0, e=0):
#         self.start = s
#         self.end = e
def getKey(interval):
    return interval.start

class Solution(object):
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
        for i,interval in enumerate(sortedIntervals):
            if i == (len(intervals)-1):
                continue
            if overlapFound:
                if overlap.end >= intervals[i+1].start: #nice lets add to interval
                    overlap.end = max(overlap.end, intervals[i+1].end)
                else:
                    retIntervals.append(overlap)
                    overlapFound = False
            else:
                if interval.end >= intervals[i+1].start: #nice lets start recording an overlap
                    overlap = Interval(interval.start, max(interval.end, intervals[i+1].end))
                    overlapFound = True
                else: #no overlap, add to ret list
                    retIntervals.append(interval)
        #add overlap if needed, else add last
        if overlapFound:
            retIntervals.append(overlap)
        elif len(sortedIntervals) > 0:
            retIntervals.append(sortedIntervals[len(sortedIntervals)-1])
        return retIntervals
        