class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        digitsLetters = dict({'2':'abc', '3':'def', '4':'ghi', '5':'jkl', '6':'mno', '7':'pqrs', '8':'tuv', '9':'wxyz'})
        ret = []
        for d in digits:
            if not ret:
                ret = [_ for _ in digitsLetters[d]]
            else:
                newret = []
                for retelem in ret:
                    for appendchar in digitsLetters[d]:
                        newret.append(retelem + appendchar) 
                ret = newret
        return ret
