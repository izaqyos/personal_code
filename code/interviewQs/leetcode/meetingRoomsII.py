"""
LC 253 - Meeting Rooms II (Medium)

Given an array of meeting time intervals where intervals[i] = [start_i, end_i],
return the minimum number of conference rooms required.

A meeting that ends at time t and a meeting that starts at time t do NOT overlap
(the room is free again at t).

Example 1:
    Input: intervals = [[0,30],[5,10],[15,20]]
    Output: 2

Example 2:
    Input: intervals = [[7,10],[2,4]]
    Output: 1

Constraints:
    1 <= intervals.length <= 10^4
    0 <= start_i < end_i <= 10^6
"""
from typing import List
import heapq


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        min_end_times_heap = []
        heapq.heappush(min_end_times_heap, intervals[0][1])

        for start, end in intervals[1:]:
            if min_end_times_heap[0] <= start:
                #great, we can reuse room so we pop the prev meeting
                heapq.heappop(min_end_times_heap)
            # we push new rooms to heap, note every elem in heap represents room used. why?
            # b.c on every room that can be reused we pop from heap left in heap only meetings
            # that require extra room (meaning push w/o pop)
            heapq.heappush(min_end_times_heap, end)

        return len(min_end_times_heap)



if __name__ == "__main__":
    s = Solution()
    cases = [
        # (intervals, expected, label)
        ([[0, 30], [5, 10], [15, 20]], 2, "example 1"),
        ([[7, 10], [2, 4]], 1, "example 2: disjoint, unsorted"),
        ([[1, 5]], 1, "single meeting"),
        ([[1, 5], [5, 10]], 1, "back-to-back: end == start reuses the room"),
        ([[1, 10], [2, 9], [3, 8], [4, 7]], 4, "fully nested"),
        ([[1, 3], [2, 4], [3, 5], [4, 6]], 2, "staggered chain"),
        ([[0, 5], [0, 5], [0, 5]], 3, "identical meetings"),
        ([[9, 10], [4, 9], [4, 17]], 2, "unsorted, back-to-back inside"),
        ([[i, i + 2] for i in range(0, 10000, 1)], 2, "10k staggered, overlap of 2"),
    ]
    passed = 0
    for intervals, exp, label in cases:
        got = s.minMeetingRooms([iv[:] for iv in intervals])
        assert got == exp, f"FAIL [{label}]: expected {exp}, got {got}"
        passed += 1
    print(f"All {passed}/{len(cases)} tests passed")
