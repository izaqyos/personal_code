"""
LC 875 - Koko Eating Bananas (Medium)

Koko loves to eat bananas. There are n piles of bananas, the i-th pile has
piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she
chooses some pile of bananas and eats k bananas from that pile. If the pile
has less than k bananas, she eats all of them instead and will not eat any
more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas
before the guards return.

Return the minimum integer k such that she can eat all the bananas within h
hours.

Example 1:
    Input: piles = [3,6,7,11], h = 8
    Output: 4

Example 2:
    Input: piles = [30,11,23,4,20], h = 5
    Output: 30

Example 3:
    Input: piles = [30,11,23,4,20], h = 6
    Output: 23

Constraints:
    1 <= piles.length <= 10^4
    piles.length <= h <= 10^9
    1 <= piles[i] <= 10^9
"""
from typing import List
from math import ceil


def minEatingSpeed(piles: List[int], h: int) -> int:
    max_pile = max(piles)
    lo, hi = 1, max_pile # k (minEatingSpeed) can't be 0 (never finish), capped at max_pile (no gain beyond)

    # binary search k. why b/c hours(k) is monotonically non increasing (eat faster finish faster jj)
    # so feasible(k) (T/F k speed finish in h hours) is monotonically rising (F, F, F then at min k true)
    # feasible k means sum(ceil(p[i]/k))<=h , 2. monotonicity, for k+1 the sum is <=, meaning sum(ceil(p[i]/(k+1)))<= sum(ceil(p[i]/k)) 
    
    while lo < hi:
        mid = (lo + hi) // 2 # must floor so we shrink on edge case lo=hi-1 , if we ceil we get mid=hi inf loop
        hours = sum( ceil(elem/mid) for elem in piles )
        if hours > h:
            lo = mid + 1
        else:
            hi = mid
    return lo



if __name__ == "__main__":
    assert minEatingSpeed([3,6,7,11], 8) == 4
    assert minEatingSpeed([30,11,23,4,20], 5) == 30
    assert minEatingSpeed([30,11,23,4,20], 6) == 23
    assert minEatingSpeed([1], 1) == 1
    assert minEatingSpeed([1,1,1,1], 4) == 1
    assert minEatingSpeed([1000000000], 2) == 500000000
    assert minEatingSpeed([312884470], 968709470) == 1
    assert minEatingSpeed([805306368,805306368,805306368], 1000000000) == 3

    print("All tests passed.")
