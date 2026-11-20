"""
LC 973 - K Closest Points to Origin (Medium)

Given an array of points where points[i] = [x_i, y_i] represents a point on the X-Y plane
and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance
(i.e., sqrt((x1 - x2)^2 + (y1 - y2)^2)).

You may return the answer in any order. The answer is guaranteed to be unique
(except for the order that it is in).

Example 1:
    Input: points = [[1,3],[-2,2]], k = 1
    Output: [[-2,2]]
    Explanation:
    The distance between (1, 3) and the origin is sqrt(10).
    The distance between (-2, 2) and the origin is sqrt(8).
    Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.

Example 2:
    Input: points = [[3,3],[5,-1],[-2,4]], k = 2
    Output: [[3,3],[-2,4]]
    Explanation: The answer [[-2,4],[3,3]] would also be accepted.

Constraints:
    1 <= k <= points.length <= 10^4
    -10^4 <= x_i, y_i <= 10^4
"""
from typing import List
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        return heapq.nsmallest(k, points, key=lambda point: point[0]*point[0] + point[1]*point[1]) 


if __name__ == "__main__":
    s = Solution()
    cases = [
        # (points, k, expected, label)  -- order doesn't matter, so compare sorted
        ([[1, 3], [-2, 2]], 1, [[-2, 2]], "example 1"),
        ([[3, 3], [5, -1], [-2, 4]], 2, [[3, 3], [-2, 4]], "example 2"),
        ([[0, 0]], 1, [[0, 0]], "single point at origin"),
        ([[1, 1], [2, 2], [3, 3]], 3, [[1, 1], [2, 2], [3, 3]], "k == n: return all"),
        ([[-5, 0], [0, 4], [3, 0]], 1, [[3, 0]], "negatives and axes"),
        ([[10000, 10000], [-10000, -10000], [1, -1]], 1, [[1, -1]], "large coordinates"),
        ([[2, 0], [0, 3], [1, 1], [-1, -1], [4, 4]], 3, [[2, 0], [1, 1], [-1, -1]], "mixed"),
    ]
    passed = 0
    for points, k, exp, label in cases:
        got = s.kClosest([p[:] for p in points], k)
        assert got is not None and sorted(map(tuple, got)) == sorted(map(tuple, exp)), \
            f"FAIL [{label}]: expected {exp} (any order), got {got}"
        passed += 1
    print(f"All {passed}/{len(cases)} tests passed")
