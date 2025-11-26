class Solution:

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = dict()
        for st in strs:
            stl = sorted(st)
            k = "".join(stl)
            if k in anagrams:
                anagrams[k].append(st)
            else:
                anagrams[k] = [st]

        return [ v for v in anagrams.values()]
