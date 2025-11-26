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
        
    def buildCharDict(self, s: str):
        s_char_dict = {}
        for i,c in enumerate(s):
            if not c in s_char_dict:
                s_char_dict[c] = [i]
            else:
                s_char_dict[c].append(i)
        return s_char_dict

    def numMatchingSubseq(self, s: str, words: List[str]) -> int:
        cnt = 0
        for word in words:
            s_char_dict = self.buildCharDict(s)
            last_match_pos=-1
            i = 0
            while i<len(word):
                c = word[i]
                if not c in s_char_dict or not s_char_dict[c]:
                    break
                else:
                    j = s_char_dict[c].pop(0) #todo, pop doesn't work if we didn't pop we can run into backward index. need to do binary search for 1st index >= last_match_pos
                    while j<=last_match_pos:
                        if not c in s_char_dict or not s_char_dict[c]:
                            j = -1
                            break
                        j = s_char_dict[c].pop(0) 
                    if j == -1:
                        break
                    else:
                        last_match_pos = j
                i+=1
            if i == len(word):
                #print(f"{word} found using optimized search")
                cnt+=1
        return cnt

    def numMatchingSubseqNaive(self, s: str, words: List[str]) -> int:
        cnt = 0
        for word in words:
            if self.issubsequence(s, word):
                #print(f"{word} found using naive search")
                cnt+=1
        return cnt