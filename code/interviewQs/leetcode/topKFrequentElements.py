"""
347. Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Constraints:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array]
- It is guaranteed that the answer is unique.

Follow up: Your algorithm's time complexity must be better than O(n log n).

Example 1: nums = [1,1,1,2,2,3], k = 2 -> [1,2]
Example 2: nums = [1], k = 1 -> [1]
"""

from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # I'll use dict num:freq and then bucket sort freq->[nums] 
    freq_counter = Counter(nums) 
    bucket: list[list[int]] = [[]  for _ in range(len(nums) +1) ]  # max freq is n so bucket len is n+1 as freq is index
    for number,frequency in freq_counter.items():
        bucket[frequency].append(number)

    ret_list: list[int] = []
    num_collected = 0
    for i in range(len(bucket)-1,-1, -1):
        if bucket[i]:
            ret_list.extend(bucket[i])
            num_collected += len(bucket[i])
        if num_collected >= k:
            return ret_list[:k]

    return ret_list


def top_k_frequent_heap(nums: list[int], k: int) -> list[int]:
    # Min heap approach — O(n log k) time, O(k) space (heap never exceeds size k)
    #
    # Hints:
    # 1. Count frequencies the same way (Counter)
    # 2. Use heapq to maintain a min heap of size k
    #    - Push (freq, num) tuples
    #    - When heap size > k, pop the smallest — this evicts the least frequent
    # 3. After processing all entries, the heap holds the k most frequent
    # 4. Why min heap and not max? Think about which element you want to discard
    #
    # heapq cheat sheet:
    #   import heapq
    #   heapq.heappush(heap, item)   — push item, heap stays sorted
    #   heapq.heappop(heap)          — pop smallest item
    #   heapq.heappushpop(heap, item) — push then pop in one op (faster combo)
    #   heapq.nlargest(k, iterable)  — k largest (uses heap internally, but not O(k) space)
    #   heap[0]                      — peek at smallest without popping
    #   heapq sorts tuples by first element, then second as tiebreaker
    #
    # Tradeoff vs bucket sort:
    #   Bucket sort: O(n) time, O(n) space (allocates n+1 buckets)
    #   Heap:        O(n log k) time, O(k) space (heap capped at k)
    #   Heap wins on space when k << n
    pass


if __name__ == "__main__":
    tests = [
        ([1, 1, 1, 2, 2, 3], 2, [1, 2]),
        ([1], 1, [1]),
        ([1, 2], 2, [1, 2]),                        # k == unique count
        ([3, 3, 3, 1, 1, 2], 1, [3]),               # single most frequent
        ([1, 1, 2, 2, 3, 3], 3, [1, 2, 3]),         # all same frequency
        ([-1, -1, -1, 2, 2], 1, [-1]),              # negatives
        ([4, 4, 4, 4, 1, 2, 3], 2, [4, 1]),         # one dominant element
        ([1, 2, 3, 4, 5, 5, 5, 5], 3, [5, 1, 2]),   # k=3, ties broken arbitrarily
    ]
    for i, (nums, k, expected) in enumerate(tests):
        result = top_k_frequent(nums, k)
        status = "PASS" if sorted(result) == sorted(expected) else "FAIL"
        print(f"Test {i+1}: {status} | nums={nums}, k={k}, expected={expected}, got={result}")
