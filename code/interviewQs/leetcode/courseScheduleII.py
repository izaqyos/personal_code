"""
LC 210 - Course Schedule II (Medium)

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [a_i, b_i] indicates that you
must take course b_i first if you want to take course a_i.

For example, the pair [0, 1] indicates that to take course 0 you have to first take course 1.

Return the ordering of courses you should take to finish all courses. If there are many valid
answers, return any of them. If it is impossible to finish all courses, return an empty array.

Example 1:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: [0,1]

Example 2:
    Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    Output: [0,2,1,3]   (also valid: [0,1,2,3])

Example 3:
    Input: numCourses = 1, prerequisites = []
    Output: [0]

Constraints:
    1 <= numCourses <= 2000
    0 <= prerequisites.length <= numCourses * (numCourses - 1)
    prerequisites[i].length == 2
    0 <= a_i, b_i < numCourses
    a_i != b_i
    All the pairs [a_i, b_i] are distinct.
"""
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        I'll run Khan topological sort, which is a BFS that returns a valid order of nodes in a DAG.
        """
        graph_representation = [[] for _ in range(numCourses)]
        ec_count = [0] * numCourses  # edge count for each node

        # I keep in comment b/c I want to show that the two conditions are equivalent: if all edges are processed, then all courses are processed, and vice versa.
        #total_ec = len(prerequisites)  # total number of edges in the graph
        bfs_queue = []
        for course, prereq in prerequisites:
            graph_representation[prereq].append(course)
            ec_count[course] += 1

        # initialize the queue with all courses that have no prerequisites
        for i in range(numCourses):
            if ec_count[i] == 0:
                bfs_queue.append(i)

        order = []
        
        while bfs_queue:
            course = bfs_queue.pop()
            order.append(course)
            for adj in graph_representation[course]:
                ec_count[adj] -= 1  
                #total_ec -= 1  
                if ec_count[adj] == 0:
                    bfs_queue.append(adj)  # If no more prerequisites, add to queue

        # Both conditions are equivalent: if all edges are processed, then all courses are processed, and vice versa.
        #return order if total_ec == 0 else []  # If all edges are processed, return order, else empty list
        return order if len(order) == numCourses else []  # If all courses are processed, return order, else empty list


def is_valid_order(n: int, prereqs: List[List[int]], order: List[int]) -> bool:
    """Any valid answer is accepted: a permutation of 0..n-1 where every prereq comes first."""
    if sorted(order) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[b] < pos[a] for a, b in prereqs)


if __name__ == "__main__":
    s = Solution()
    cases = [
        # (numCourses, prerequisites, possible?, label)
        (2, [[1, 0]], True, "example 1"),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True, "example 2: diamond"),
        (1, [], True, "example 3: single course"),
        (3, [], True, "no prereqs: any permutation"),
        (2, [[1, 0], [0, 1]], False, "2-cycle"),
        (4, [[1, 0], [2, 1], [3, 2]], True, "chain"),
        (4, [[1, 0], [2, 1], [3, 2], [1, 3]], False, "cycle not through node 0"),
        (5, [[1, 0], [0, 1], [3, 4]], False, "disconnected: one component cyclic"),
        (6, [[1, 0], [2, 1], [4, 3], [5, 4]], True, "two independent chains"),
        (2000, [[i + 1, i] for i in range(1999)], True, "long chain (recursion depth)"),
        (2000, [[i + 1, i] for i in range(1999)] + [[0, 1999]], False, "long cycle"),
    ]
    passed = 0
    for n, pre, possible, label in cases:
        got = s.findOrder(n, pre)
        if possible:
            assert got is not None and is_valid_order(n, pre, got), f"FAIL [{label}]: invalid order {got}"
        else:
            assert got == [], f"FAIL [{label}]: expected [], got {got}"
        passed += 1
    print(f"All {passed}/{len(cases)} tests passed")
