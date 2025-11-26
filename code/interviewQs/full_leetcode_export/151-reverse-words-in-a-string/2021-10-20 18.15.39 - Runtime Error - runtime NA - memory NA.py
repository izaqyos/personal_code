class Solution:
    def reverseWords(self, s: str) -> str:
        return s.split()[::-1].join(" ")