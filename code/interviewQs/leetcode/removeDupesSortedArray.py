"""
Given a sorted array nums, remove the duplicates in-place such that duplicates appeared at most twice and return the new length.

Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory.

Example 1:

Given nums = [1,1,1,2,2,3],

Your function should return length = 5, with the first five elements of nums being 1, 1, 2, 2 and 3 respectively.

It doesn't matter what you leave beyond the returned length.
Example 2:

Given nums = [0,0,1,1,1,1,2,3,3],

Your function should return length = 7, with the first seven elements of nums being modified to 0, 0, 1, 1, 2, 3 and 3 respectively.

It doesn't matter what values are set beyond the returned length.
Clarification:

Confused why the returned value is an integer but your answer is an array?

Note that the input array is passed in by reference, which means modification to the input array will be known to the caller as well.

Internally you can think of this:

// nums is passed in by reference. (i.e., without making a copy)
int len = removeDuplicates(nums);

// any modification to nums in your function would be known by the caller.
// using the length returned by your function, it prints the first len elements.
for (int i = 0; i < len; i++) {
    print(nums[i]);
}
"""

class Solution:
    def removeDuplicates(self, nums):
        """
        idea, run two indices. running and latest
        swap latest (non valid address) with next valid
        validity condition. repeat < 3.
        note. sorted means if we have three elements. a1,a2,a3 if a3==a1 => a3==a2. so we can skip one comparison
        """
        n = len(nums)
        if n<3:
            return n

        last = 2
        for i in range(2,n):
            if nums[i]!=nums[last-2]:
                nums[last],nums[i] = nums[i], nums[last]
                last+=1
        return last


    #def removeDuplicates(self, nums):
    #    if len(nums) <=2:
    #        return len(nums)

    #    last = 1
    #    repeat = 1
    #    prev = nums[0]
    #    for i in range(1, len(nums)): #i is current
    #        print('i={}, l={}, r={}, prev={}'.format(i, last, repeat, prev))
    #        if prev == nums[i]:
    #            repeat +=1
    #        else:
    #            repeat = 1
    #        prev = nums[i]
    #        if repeat < 3:
    #            if last < i:
    #                print('swap indices {}<->{}'.format(last, i))
    #                nums[last], nums[i] = nums[i], nums[last]
    #            print('last+1')
    #            last +=1
    #        
    #    return last-1

def test():
    inputs = [
        [],
        [1],
        [1,1,1,2],
        [1,1,1,2,2,3],
        [0,0,1,1,1,1,2,3,3],
        [1,1,1,2,2,3],
    ]
    expected = [
        ([], 0),
        ([1], 1),
        ([1,1,2], 3),
        ([1,1,2,2,3], 5),
        ([0,0,1,1,2,3,3], 7),
        ([1,1,2,2,3], 5),
    ]

    sol = Solution()
    for inp,exp in zip (inputs, expected):
        print('input', inp)
        length = sol.removeDuplicates(inp)
        print('output={}, len={}'.format(inp, length))
        assert(length == exp[1])
        assert(inp[:length] == exp[0])


if __name__ == "__main__":
    test()
        
