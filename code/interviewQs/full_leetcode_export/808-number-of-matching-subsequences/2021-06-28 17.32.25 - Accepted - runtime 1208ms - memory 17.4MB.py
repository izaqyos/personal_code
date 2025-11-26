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
        s_char_dict = self.buildCharDict(s)
        for word in words:
            already_matched_position = { k:-1 for k in s_char_dict.keys()}  
            last_match_pos=-1
            i = 0
            while i<len(word):
                c = word[i]
                if not c in s_char_dict or not s_char_dict[c]:
                    break
                else:
                    found_pos = -1
                    for j in  s_char_dict[c]:
                        #print(c, s_char_dict[c], j, last_match_pos, already_matched_position[c])
                        if j<=last_match_pos or j <= already_matched_position[c]:
                            continue
                        already_matched_position[c] = j
                        found_pos = j
                        break
                    #print(c, found_pos)
                    if found_pos == -1:
                        break
                    else:
                        last_match_pos = found_pos
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