"""
LC 2050. Parallel Courses III (Hard) -- the Amazon 18/10 problem, redone

You are given an integer n, which indicates that there are n courses labeled from 1 to n.
You are also given a 2D integer array relations where relations[j] = [prevCourse_j, nextCourse_j]
denotes that course prevCourse_j has to be completed before course nextCourse_j (prerequisite
relationship). Furthermore, you are given a 0-indexed integer array time where time[i] denotes
how many months it takes to complete the (i+1)th course.

You must find the minimum number of months needed to complete all the courses following these rules:
    - You may start taking a course at any time if the prerequisites are met.
    - Any number of courses can be taken at the same time.

Return the minimum number of months needed to complete all the courses.
Note: The test cases are generated such that it is possible to complete every course
(i.e., the graph is a directed acyclic graph).

Example 1:
    Input: n = 3, relations = [[1,3],[2,3]], time = [3,2,5]
    Output: 8
    Explanation: Start courses 1 and 2 at month 0. Course 1 takes 3 months, course 2 takes 2.
    Course 3 can start at month 3 and takes 5 more months: 3 + 5 = 8.

Example 2:
    Input: n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
    Output: 12
    Explanation: Courses 1, 2, 3 start at month 0 and finish at months 1, 2, 3.
    Course 4 starts at 3, finishes at 7. Course 5 starts at max(1, 2, 3, 7) = 7, finishes at 12.

Constraints:
    1 <= n <= 5 * 10^4
    0 <= relations.length <= min(n * (n - 1) / 2, 5 * 10^4)
    relations[j].length == 2
    1 <= prevCourse_j, nextCourse_j <= n
    prevCourse_j != nextCourse_j
    All the pairs [prevCourse_j, nextCourse_j] are unique.
    time.length == n
    1 <= time[i] <= 10^4
    The given graph is a directed acyclic graph.

Before coding (the habit from 18/10): state the time formula, then test it by hand on the
"uneven" case below (a short chain next to one long course) before writing a line.

my idea Khan BFS plus finish times (init to start times then update to finish)
what I need:
deque, defaultdict(list) graph where graph[u]=[v1,v2] u->v1, u>v2 
given no cycles so I don't need visited set
ec list where ec[i] incoming edge count i 
fin_t=[0 for _ in courses] #start as wait time 
push all ec[i]==0 to Q and run BFS
while Q 
    pop u
    fin_t[u] += time[u] #final no deps for u as it only pushed when ec==0
    for v in graph[u]:
        fin_t[v] = max(fin_t[v], fin_t[u]) # v must wait longest dep 
        ec[v] -= 1
        if ec[v] == 0:
         push v 2 Q

return max(fin_t)
"""
from typing import List
from collections import defaultdict
from collections import deque


def minimumTime(n: int, relations: List[List[int]], time: List[int]) -> int:
    graph = defaultdict(list)
    bfs_q = deque()
    ec=[0]*(n+1) #0 dumm cell for normalized access. edge count, how many deps does node v have
    fin_t=[0]*(n+1) # starts as wait time but after popping from Q updates to finish time
    normalized_time = [0]+time

    # build graph and edge count
    for u, v in relations:
        ec[v] +=1
        graph[u].append(v)

    for v, edge_count in enumerate(ec):
        if edge_count == 0:
            bfs_q.append(v)

    while bfs_q:
        cur_vert = bfs_q.popleft()
        fin_t[cur_vert] += normalized_time[cur_vert]
        for neigbor in graph[cur_vert]:
            fin_t[neigbor] = max(fin_t[neigbor], fin_t[cur_vert])
            ec[neigbor] -=1
            if ec[neigbor] == 0:
                bfs_q.append(neigbor)

    return max(fin_t)

    


if __name__ == "__main__":
    tests = [
        ((3, [[1, 3], [2, 3]], [3, 2, 5]), 8, "example 1"),
        ((5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]), 12, "example 2"),
        ((3, [[1, 3]], [1, 10, 1]), 10, "uneven: short chain next to a long course (the 18/10 bug)"),
        ((1, [], [7]), 7, "single course"),
        ((4, [], [4, 1, 9, 2]), 9, "no relations: all in parallel"),
        ((4, [[1, 2], [2, 3], [3, 4]], [1, 2, 3, 4]), 10, "one chain"),
        ((5, [[1, 2], [2, 3], [4, 5]], [1, 1, 1, 5, 1]), 6, "two chains, unequal"),
        ((4, [[1, 2], [1, 3], [2, 4], [3, 4]], [1, 5, 1, 1]), 7, "diamond"),
    ]
    passed = 0
    for (n, rel, t), exp, label in tests:
        got = minimumTime(n, [r[:] for r in rel], t[:])
        assert got == exp, f"FAIL [{label}]: expected {exp}, got {got}"
        passed += 1

    # randomized check against a brute-force longest-path oracle on random DAGs
    import random
    from functools import lru_cache
    random.seed(2050)
    for trial in range(300):
        n = random.randint(1, 9)
        order = list(range(1, n + 1))
        random.shuffle(order)
        rel = [[order[i], order[j]] for i in range(n) for j in range(i + 1, n) if random.random() < 0.3]
        t = [random.randint(1, 10) for _ in range(n)]
        preds = {v: [u for u, w in rel if w == v] for v in range(1, n + 1)}

        @lru_cache(None)
        def finish(v):
            return t[v - 1] + max((finish(u) for u in preds[v]), default=0)

        exp = max(finish(v) for v in range(1, n + 1))
        got = minimumTime(n, [r[:] for r in rel], t[:])
        assert got == exp, f"FAIL random #{trial}: n={n} rel={rel} t={t} expected {exp}, got {got}"
        passed += 1
    print(f"All {passed} tests passed")
