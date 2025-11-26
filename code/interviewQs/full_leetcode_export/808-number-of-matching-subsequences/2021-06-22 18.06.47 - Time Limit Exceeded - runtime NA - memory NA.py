class Solution:
    def issubsequence(self, s: str, word: str) -> bool:
        if len(s) < len(word):
            return False
        i=0
        j=0
        while i<len(word):
            c = word[i]
            while j<len(s):
                if c != s[j]:
                    j+=1
                else:
                    break
            if j>=len(s):
                return False
            i+=1
            j+=1
        if i==len(word):
            return True
        
    def numMatchingSubseq(self, s: str, words: List[str]) -> int:
        cnt = 0
        for word in words:
            if self.issubsequence(s, word):
                cnt+=1
        return cnt
        