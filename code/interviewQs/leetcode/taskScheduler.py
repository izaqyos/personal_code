"""
LC 621. Task Scheduler (Medium)

You are given an array of CPU tasks, each labeled with a letter from A to Z, and a number n.
Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in
any order, but there's a constraint: there has to be a gap of at least n intervals between two
tasks with the same label.

Return the minimum number of CPU intervals required to complete all tasks.

Example 1:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation: A -> B -> idle -> A -> B -> idle -> A -> B

Example 2:
    Input: tasks = ["A","C","A","B","D","B"], n = 1
    Output: 6
    Explanation: A -> B -> C -> D -> A -> B

Example 3:
    Input: tasks = ["A","A","A","B","B","B"], n = 3
    Output: 10
    Explanation: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B

Constraints:
    1 <= tasks.length <= 10^4
    tasks[i] is an uppercase English letter.
    0 <= n <= 100
"""

from collections import Counter
import heapq

def least_interval(tasks: list[str], n: int) -> int:
    job_counts = Counter(tasks) #O(1) space and O(n) ctor time
    counts_max_heap=[]
    intervals = 0

    # O(1) run time, 26 max jobs, log(26)*26
    heapq.heapify([-cnt for cnt in job_counts.values()])

    # runs N times
    while counts_max_heap:
        #lets pop n+1 jobs if possible to get optimal idle free sequence 
        popped = []
        for _ in range(n+1):
            if counts_max_heap:
                popped.append(-heapq.heappop(counts_max_heap))
                intervals += 1
            else:
                break
        if max(popped) > 1: #not last round, as in last round all job counts are 0 (the 1 is from prev round)
            intervals += n+1 - len(popped)
            for cnt in popped:
                cnt -= 1
                if cnt>0:
                    heapq.heappush(counts_max_heap, -cnt)
            
    return intervals
        
                




if __name__ == "__main__":
    cases = [
        (["A", "A", "A", "B", "B", "B"], 2, 8),
        (["A", "C", "A", "B", "D", "B"], 1, 6),
        (["A", "A", "A", "B", "B", "B"], 3, 10),
        (["A", "A", "A", "B", "B", "B"], 0, 6),
        (["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2, 16),
        (["A"], 5, 1),
        (["A", "A"], 5, 7),
        (["A", "A", "A", "B", "B", "B", "C", "C", "C", "D", "D", "E"], 2, 12),
    ]
    passed = 0
    for tasks, n, expected in cases:
        got = least_interval(tasks, n)
        assert got == expected, f"tasks={tasks} n={n}: expected {expected}, got {got}"
        passed += 1
    print(f"{passed}/{len(cases)} passed")
