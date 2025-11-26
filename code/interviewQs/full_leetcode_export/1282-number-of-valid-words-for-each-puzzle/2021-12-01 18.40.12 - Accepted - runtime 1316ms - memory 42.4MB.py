class Solution:
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        def bitmask(w):
            m=0
            for c in w:
                m |=1<<ord(c)-ord('a')
            return m

        word_masks= Counter(bitmask(word) for word in words) 
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
