"""
11. Container With Most Water
https://leetcode.com/problems/container-with-most-water/

You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

Example 1: height = [1,8,6,2,5,4,8,3,7] -> 49  (between index 1 and 8)
Example 2: height = [1,1] -> 1
"""


def max_area(height: list[int]) -> int:
    if not height or len(height) == 1:
        return 0
    
    n = len(height)
    global_area = 0
    lptr, rptr = 0,  n-1 
    while lptr < rptr:
        width = rptr - lptr
        local_area = width * min(height[lptr], height[rptr])
        max_area = max(global_area, local_area)
        # always advance shorter. if we move higher line, we can never get a higher area.
        if (height[lptr] < height[rptr]):
            lptr +=1
        else:
            rptr -=1


    return global_area



if __name__ == "__main__":
    tests = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),          # equal heights at edges
        ([1, 2, 1], 2),                  # small array
        ([1, 2, 4, 3], 4),              # max isn't at the widest
        ([2, 3, 4, 5, 18, 17, 6], 17),  # tall lines close together
        ([1, 1, 1, 1, 1], 4),           # all same height
        ([0, 2], 0),                     # one zero height
        ([10000, 10000], 10000),         # max height constraint
    ]
    for i, (height, expected) in enumerate(tests):
        result = max_area(height)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i+1}: {status} | height={height}, expected={expected}, got={result}")
