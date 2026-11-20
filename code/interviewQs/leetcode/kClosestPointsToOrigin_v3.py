"""
LC 973 - K Closest Points to Origin (Medium) -- v3: quickselect

FOLLOW-UP RULES (interviewer: "can you beat O(n log k)?"):
  - Quickselect: no heapq, no sorted / list.sort.
  - Rearrange `points` in place; return the first k.
  - Target: O(n) average time, O(1) extra space (excluding recursion, if you recurse).
  - Use a random pivot.

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
import random


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        quickselect version. avg O(n) time, O(1) extra space (no recursion stack - I'll impl iteratively).
        """
        left, right= 0, len(points) - 1
        # partition points into < pivot_dist and >= pivot_dist
        while left <= right:
            pivot_idx = random.randint(left, right)
            pivot_dist = points[pivot_idx][0] ** 2 + points[pivot_idx][1] ** 2
            # 3 way partition 
            l = left #left wall of == pivot_dist slice
            i = l #scanner
            r=right #right wall unexplored slice

            while i<=r:
                cur_dist = points[i][0] ** 2 + points[i][1] ** 2
                if cur_dist > pivot_dist: #swap 2 right side
                    points[r], points[i] = points[i], points[r] #elem in final location
                    r -= 1 
                elif cur_dist < pivot_dist:
                    #we swap cur and left before advancing both
                    #since we want smaller elem in the slice to the left side of left (the < pivot slice)
                    points[l], points[i] = points[i], points[l] #elem in final location
                    l += 1
                    i +=1
                else: #equal
                    i +=1
            # invariant [l..r] exact sorted range of pivot
            if l<=k<=r+1:
                return points[:k]
            elif k<l: #k is in the left side so partition to search it now
                right = l-1
            else:
                left = r+1
        return None
            




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
    # randomized check against a brute-force oracle (ties avoided: answer must be unique)
    import random
    random.seed(973)
    for t in range(200):
        n = random.randint(1, 60)
        pts = [[random.randint(-50, 50), random.randint(-50, 50)] for _ in range(n)]
        k = random.randint(1, n)
        d = sorted(x * x + y * y for x, y in pts)
        if k < n and d[k - 1] == d[k]:
            continue  # tie at the cut-off -> not a unique answer
        exp = sorted(map(tuple, pts), key=lambda p: p[0] * p[0] + p[1] * p[1])[:k]
        got = s.kClosest([p[:] for p in pts], k)
        assert got is not None and sorted(map(tuple, got)) == sorted(exp), f"FAIL random #{t}: {pts} k={k} got {got}"
        passed += 1
    print(f"All {passed} tests passed")
