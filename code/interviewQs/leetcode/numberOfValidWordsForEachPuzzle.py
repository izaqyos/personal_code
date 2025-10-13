"""
Number of Valid Words for Each Puzzle
With respect to a given puzzle string, a word is valid if both the following conditions are satisfied:
word contains the first letter of puzzle.
For each letter in word, that letter is in puzzle.
For example, if the puzzle is "abcdefg", then valid words are "faced", "cabbage", and "baggage", while
invalid words are "beefed" (does not include 'a') and "based" (includes 's' which is not in the puzzle).
Return an array answer, where answer[i] is the number of words in the given word list words that is valid with respect to the puzzle puzzles[i].
 


Example 1:

Input: words = ["aaaa","asas","able","ability","actt","actor","access"], puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"]
Output: [1,1,3,2,4,0]
Explanation: 
1 valid word for "aboveyz" : "aaaa" 
1 valid word for "abrodyz" : "aaaa"
3 valid words for "abslute" : "aaaa", "asas", "able"
2 valid words for "absoryz" : "aaaa", "asas"
4 valid words for "actresz" : "aaaa", "asas", "actt", "access"
There are no valid words for "gaswxyz" cause none of the words in the list contains letter 'g'.
Example 2:

Input: words = ["apple","pleas","please"], puzzles = ["aelwxyz","aelpxyz","aelpsxy","saelpxy","xaelpsy"]
Output: [0,1,3,2,0]
 

Constraints:

1 <= words.length <= 105
4 <= words[i].length <= 50
1 <= puzzles.length <= 104
puzzles[i].length == 7
words[i] and puzzles[i] consist of lowercase English letters.
Each puzzles[i] does not contain repeated characters.
"""

from collections import Counter
class Solution:
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        def bitmask(w):
            # we don't care about repeates, just if char is in word, so we toggle 1 bit per character (only 26 so 32 bit more than enough
            m=0
            for c in w:
                m |=1<<ord(c)-ord('a')
            return m

        word_masks= Counter(bitmask(word) for word in words)  #counter dictionary for all bitmasks
        res = []
        for puzzle in puzzles:
            firstCharBit=1<<(ord(puzzle[0])- ord('a'))
            puzzle_count = word_masks[firstCharBit] #words that contain the first letter of puzzle only

            puzzlemask = bitmask(puzzle[1:]) # we take the bitmask minus first bit since it must be there we will add it at each match check

            submask = puzzlemask 
            while submask:
                puzzle_count += word_masks[submask|firstCharBit]
                submask = (submask-1)&puzzlemask #this trick finds all subsets of mask. how?- 2 conditions. a. if we substract 1 from mask to 0 we will get all subsets (but also non subsets) and b. to sift out non subsets of mask we & with mask. 
            res.append(puzzle_count)
        return res

    def findNumOfValidWordsNaive(self, words: List[str], puzzles: List[str]) -> List[int]:
        """
        Naive Solution. TLE
        """
        ret=[0 for _ in puzzles]
        puzzles_chardicts=[{k:len(p)-1-i for i,k in enumerate(p[::-1])} for p in puzzles]
        #print(puzzles_chardicts)
        for i,puzzle_dict in enumerate(puzzles_chardicts):
            matches = 0
            for word in words:
                matched = False
                for c in word:
                    if not c in puzzle_dict :
                        matched = False #we want to reset flag to indicate match failure
                        break
                    else:
                        if puzzle_dict[c] == 0:
                            matched = True #it's not really final decision. any non matching char will set math to False
                if matched:
                    matches += 1
            ret[i] = matches
        return ret


"""
Good Solution with Explanation:
    https://leetcode.com/problems/number-of-valid-words-for-each-puzzle/discuss/1567324/C%2B%2BPython-Clean-Solutions-w-Detailed-Explanation-or-Bit-masking-and-Trie-Approaches
    https://leetcode.com/problems/number-of-valid-words-for-each-puzzle/solution/
Adding all of the steps together, for each puzzle, we just need to iterate over all the subsets of letters contained in puzzle that also contain the first letter of puzzle. For each subset, we add the number of words that match the subset to the count of valid words for the current puzzle. Thus, for one puzzle, the complexity is O ( 2^ p u z z l e .  l e n g t h) O(2^ puzzle.length), which is much less than the total number of words in words.

Algorithm

Step 1: Build the map.

For each word in words:
Transform it into a bitmask of its characters.
If the bitmask has not been seen before, store it as a key in the map with a value of one.
If it has been seen before, then increment the map's count for this bitmask by one.
Step 2: Count the number of valid words for each puzzle.

For each puzzle in puzzles:
Transform it into a bitmask of its characters.
Iterate over every possible submask containing the first letter in puzzle (puzzle[i][0]). A word is valid for a puzzle if its bitmask matches one of the puzzle's submasks.
For each submask, increase the count by the number of words that match the submask.
We can find the number of words that match the submask using the map built in the previous step.
python textbook solution:
class Solution:
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:

        def bitmask(word: str) -> int:
            mask = 0
            for letter in word:
                mask |= 1 << (ord(letter) - ord('a'))
            return mask

        # Create a bitmask for each word.
        word_count = Counter(bitmask(word) for word in words)

        result = []
        for puzzle in puzzles:
            first = 1 << (ord(puzzle[0]) - ord('a'))
            count = word_count[first]

            # Make bitmask but ignore the first character since it must always
            # be there.
            mask = bitmask(puzzle[1:])

            # Iterate over every possible subset of characters.
            submask = mask
            while submask:
                # Increment the count by the number of words that match the
                # current submask.
                count += word_count[submask | first]  # add first character
                submask = (submask - 1) & mask
            result.append(count)
        return result
"""



