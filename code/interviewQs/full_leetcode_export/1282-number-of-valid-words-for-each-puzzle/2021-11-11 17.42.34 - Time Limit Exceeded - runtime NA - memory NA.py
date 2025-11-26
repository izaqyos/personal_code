class Solution:
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        ret=[0 for _ in puzzles]
        puzzles_chardicts=[{k:i for i,k in enumerate(p)} for p in puzzles]
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

