class Solution:
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
                    j = s_char_dict[c].pop(0)
                    if j<=last_match_pos:
                        break
                    else:
                        last_match_pos = j
                i+=1
            if i == len(word):
                cnt+=1
        return cnt
        