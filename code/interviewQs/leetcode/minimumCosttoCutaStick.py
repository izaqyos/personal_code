"""
Minimum Cost to Cut a Stick
Given a wooden stick of length n units. The stick is labelled from 0 to n. For example, a stick of length 6 is labelled as follows:
Given an integer array cuts where cuts[i] denotes a position you should perform a cut at.

You should perform the cuts in order, you can change the order of the cuts as you wish.

The cost of one cut is the length of the stick to be cut, the total cost is the sum of costs of all cuts. When you cut a stick, it will be split into two smaller sticks (i.e. the sum of their lengths is the length of the stick before the cut). Please refer to the first example for a better explanation.

Return the minimum total cost of the cuts.

 

Example 1:
Input: n = 7, cuts = [1,3,4,5]
Output: 16
Explanation: Using cuts order = [1, 3, 4, 5] as in the input leads to the following scenario:

The first cut is done to a rod of length 7 so the cost is 7. The second cut is done to a rod of length 6 (i.e. the second part of the first cut), the third is done to a rod of length 4 and the last cut is to a rod of length 3. The total cost is 7 + 6 + 4 + 3 = 20.
Rearranging the cuts to be [3, 5, 1, 4] for example will lead to a scenario with total cost = 16 (as shown in the example photo 7 + 4 + 3 + 2 = 16).
Example 2:
Input: n = 9, cuts = [5,6,1,4,2]
Output: 22
Explanation: If you try the given cuts ordering the cost will be 25.
There are much ordering with total cost <= 25, for example, the order [4, 6, 5, 2, 1] has total cost = 22 which is the minimum possible.
 

Constraints:

2 <= n <= 106
1 <= cuts.length <= min(n - 1, 100)
1 <= cuts[i] <= n - 1
All the integers in cuts array are distinct.
"""
"""
idea: 
    after we sort cuts we know that if we cut at index ind then there would be two sticks for which the problem can be solved indenpendantly. 
    Because sticks don't overlap
    ex: n=7, cuts = [1,3,4,5]
    first cut we chose is 3.
    We get 2 sticks:
        0-3 and 3-7 
    and 2 corresponding sub cuts arrays
    [1] and [4,5]
    obviously making the cut 1 will not effect 3-7 stick 
    for convenience we can add cut 0 and n to cuts array. this will help generalize the cut cost equation.
    how?
    say we add 0 and 7 to cuts.so cuts = [0,1,3,4,5,7] and i,j partitions indices are 1 and 4 
    now cost of any cut is cuts[j+1] - cuts[i-1] = 7-0 = 7
    say we cut at 4. we get:
        lower partition: [0,1,3,4] and i,j partitions indices are 1 and 2 
        lower stick [0-4], it's length is 4, cost = cuts[j+1]-cuts[i-1] = 4-0 = 4
        this example show why the cost equation is true. since cuts[j+1] is the high part of the stick and cuts[i-1] is the lower.
    Now that we have this in mind the problem becomes a simple recursion.
    we need a partition(i,j) utility function. It's pseudo code is:
        if i>j:
            return 0 #partitions are ordered lower index can't pass higher
        minimum_cost = float('inf')
        for ind in range(i, j+1): try all the cuts. remember. i-1 and j are added for convenience. they aren't real cuts
            cost = cuts[j+1] -cuts[i-1] + partition(i,ind-1)+partition(ind+1,j)
            minimum_cost = min(minimum_cost, cost)
        return minimum_cost
"""
#"""
#Naive approach. recursion. works but fails on TLE
#n =
#30
#cuts =
#[13,25,16,20,26,5,27,8,23,14,6,15,21,24,29,1,19,9,3]
#"""
#class Solution:
#    def part(self, partitions, i, j):
#        #print(f"solve partition indices {i,j}")
#        if i>j:
#            return 0
#        minimum_cost = float('inf')
#        for ind in range(i,j+1):
#            cost = partitions[j+1]-partitions[i-1] + self.part(partitions, i,ind-1)+self.part(partitions, ind+1,j)
#            minimum_cost = min(minimum_cost, cost)
#        return minimum_cost
#
#    def minCost(self, n: int, cuts: List[int]) -> int:
#        cuts.sort()
#        partitions = [0]+cuts[:]+[n] #pad cuts with 0 and len(cuts) values for convenience
#        #print(f"Claculate min cost of cutting stick of length {n} given cuts {cuts}. Created partitions array: {partitions}")
#        return self.part(partitions, 1, len(cuts)) #solve partitions min cost problem. 

"""
Memo approach. Test this:
n =
30
cuts =
[13,25,16,20,26,5,27,8,23,14,6,15,21,24,29,1,19,9,3]
"""
class Solution:
    def part(self,memo, partitions, i, j):
        #print(f"solve partition indices {i,j}")
        if i>j:
            return 0
        minimum_cost = float('inf')
        for ind in range(i,j+1):
            lower_cost, upper_cost = float('inf'), float('inf')
            if memo[i][ind-1] == -1:
                memo[i][ind-1] = self.part(memo, partitions, i,ind-1)
            lower_cost = memo[i][ind-1]
            if memo[ind+1][j] == -1:
                memo[ind+1][j] = self.part(memo, partitions, ind+1, j)
            upper_cost = memo[ind+1][j]

            cost = partitions[j+1]-partitions[i-1] + lower_cost + upper_cost
            minimum_cost = min(minimum_cost, cost)
        return minimum_cost

    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts.sort()
        partitions = [0]+cuts[:]+[n] #pad cuts with 0 and len(cuts) values for convenience
        memo =[ [-1 for _ in range(len(partitions)+1)] for _ in range(len(partitions)+1)]
        #print(f"Claculate min cost of cutting stick of length {n} given cuts {cuts}. Created partitions array: {partitions}")
        return self.part(memo, partitions, 1, len(cuts)) #solve partitions min cost problem. 

