"""
LC 207 - Course Schedule (Medium)

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [a_i, b_i] indicates that you
must take course b_i first if you want to take course a_i.

For example, the pair [0, 1] indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

Example 1:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: true
    Explanation: Take course 0, then course 1.

Example 2:
    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output: false
    Explanation: Course 1 needs course 0 and course 0 needs course 1. Impossible.

Constraints:
    1 <= numCourses <= 2000
    0 <= prerequisites.length <= 5000
    prerequisites[i].length == 2
    0 <= a_i, b_i < numCourses
    All the pairs prerequisites[i] are unique.
"""
from typing import List
from collections import deque


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph_representation = [[] for _ in range(numCourses)]
        ec_count = [0] * numCourses  # edge count for each node
        total_ec = len(prerequisites)  # total number of edges in the graph
        bfs_queue = deque()
        for course, prereq in prerequisites:
            graph_representation[prereq].append(course)
            ec_count[course] += 1

        # initialize the queue with all courses that have no prerequisites
        for i in range(numCourses):
            if ec_count[i] == 0:
                bfs_queue.append(i)

        while bfs_queue:
            course = bfs_queue.popleft()
            for adj in graph_representation[course]:
                ec_count[adj] -= 1  
                total_ec -= 1  
                if ec_count[adj] == 0:
                    bfs_queue.append(adj)  # If no more prerequisites, add to queue

        return total_ec == 0  # If all edges are processed, return True
        



if __name__ == "__main__":
    s = Solution()
    cases = [
        # (numCourses, prerequisites, expected, label)
        (2, [[1, 0]], True, "example 1"),
        (2, [[1, 0], [0, 1]], False, "example 2: 2-cycle"),
        (1, [], True, "single course, no prereqs"),
        (3, [], True, "no prereqs"),
        (1, [[0, 0]], False, "self-loop"),
        (4, [[1, 0], [2, 1], [3, 2]], True, "chain"),
        (4, [[1, 0], [2, 1], [3, 2], [1, 3]], False, "cycle not through node 0"),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True, "diamond (shared prereq, no cycle)"),
        (5, [[1, 0], [0, 1], [3, 4]], False, "disconnected: one component cyclic"),
        (6, [[1, 0], [2, 1], [4, 3], [5, 4], [3, 5]], False, "cycle in second component"),
        (2000, [[i + 1, i] for i in range(1999)], True, "long chain (recursion depth)"),
        (2000, [[i + 1, i] for i in range(1999)] + [[0, 1999]], False, "long cycle"),
    ]
    passed = 0
    for n, pre, exp, label in cases:
        got = s.canFinish(n, pre)
        assert got == exp, f"FAIL [{label}]: expected {exp}, got {got}"
        passed += 1
    print(f"All {passed}/{len(cases)} tests passed")
