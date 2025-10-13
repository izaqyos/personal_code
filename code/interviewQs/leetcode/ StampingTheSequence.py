""" 
Stamping The Sequence
You are given two strings stamp and target. Initially, there is a string s of length target.length with all s[i] == '?'.

In one turn, you can place stamp over s and replace every letter in the s with the corresponding letter from stamp.

For example, if stamp = "abc" and target = "abcba", then s is "?????" initially. In one turn you can:
place stamp at index 0 of s to obtain "abc??",
place stamp at index 1 of s to obtain "?abc?", or
place stamp at index 2 of s to obtain "??abc".
Note that stamp must be fully contained in the boundaries of s in order to stamp (i.e., you cannot place stamp at index 3 of s).
We want to convert s to target using at most 10 * target.length turns.

Return an array of the index of the left-most letter being stamped at each turn. If we cannot obtain target from s within 10 * target.length turns, return an empty array.
Example 1:

Input: stamp = "abc", target = "ababc"
Output: [0,2]
Explanation: Initially s = "?????".
- Place stamp at index 0 to get "abc??".
- Place stamp at index 2 to get "ababc".
[1,0,2] would also be accepted as an answer, as well as some other answers.
Example 2:

Input: stamp = "abca", target = "aabcaca"
Output: [3,0,1]
Explanation: Initially s = "???????".
- Place stamp at index 3 to get "???abca".
- Place stamp at index 0 to get "abcabca".
- Place stamp at index 1 to get "aabcaca".
 

Constraints:

1 <= stamp.length <= target.length <= 1000
stamp and target consist of lowercase English letters.

Nice submission: https://leetcode.com/problems/stamping-the-sequence/discuss/2458787/Python98.5Fastest-solution-or-Detailed-explantion-or-Easy-understand-_ 
Idea, 

a. create permutations of covers on every character in stamp. Just like this: s_covers = {'abc', 'a##', 'ab#', '#bc', '#b#', '##c'}
Ex:
In [38]: for i in range(len(s)):
    ...:     for j in range(len(s) - i):
    ...:         substr = i * "#" + s[i : len(s) - j] + "#" * j
    ...:         print(i, j, substr)
    ...:         retset.add(substr)
0 0 abcd
0 1 abc#
0 2 ab##
0 3 a###
1 0 #bcd
1 1 #bc#
1 2 #b##
2 0 ##cd
2 1 ##c#
3 0 ###d

In [39]: retset
Out[39]: 
{'###d',
 '##c#',
 '##cd',
 '#b##',
 '#bc#',
 '#bcd',
 'a###',
 'ab##',
 'abc#',
 'abcd'}


b. Keep scan through the target backwards, from end -len(stamp) to 0. Reason to search backwards is it limits the options. If we scan from start we get exponential # of options. If we find part of target is in s_covers, we store the index in a res list and cover the target with '#' to mark that we can get this part stamped If we cannot find it, it means that we cannot obtain target from stamp.

c. After the loop, target will be '#' * length of target. And we just need to reverse the res and return it.
""" 

class Solution:
    def movesToStamp(self, stamp: str, target: str) -> List[int]:
        m,n = len(stamp), len(target) 
        ret = []
        possible_stamps = set()
        for i in range(m):
            for j in range(m-i):
                possible_stamps.add(i*'#'+stamp[i:m-j]+j*'#')

        desired_target='#'*n
        while target != desired_target:
            print(target)
            found = False
            for i in range(n-m+1, -1, -1):
                if target[i:i+m] in possible_stamps:
                    target = target[:i] +m*'#'+target[i+m:]
                    ret.append(i)
                    found = True
            if not found:
                return []
        return ret[::-1]

        

""" 

code w/ prints for understanding 
class Solution:
    def movesToStamp(self, stamp: str, target: str) -> List[int]:
        m,n = len(stamp), len(target) 
        ret = []
        possible_stamps = set()
        for i in range(m):
            for j in range(m-i):
                possible_stamps.add(i*'#'+stamp[i:m-j]+j*'#')

        desired_target='#'*n
        while target != desired_target:
            print(target)
            found = False
            for i in range(n-m+1, -1, -1):
                if target[i:i+m] in possible_stamps:
                    print(f"add {i} match of {target[i:i+m]}")
                    target = target[:i] +m*'#'+target[i+m:]
                    
                    ret.append(i)
                    found = True
            if not found:
                return []
        return ret[::-1]

input:
"abca"
"aabcaca"

stdout:
aabcaca
add 1 match of abca
add 0 match of a###
#####ca
add 3 match of ##ca

Output
[3,0,1]
Expected
[3,0,1]
"""
