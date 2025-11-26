class Solution(object):
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """
        try: 
            lastWord =  s.strip().split(" ")[-1]
        except IndexError:
            return 0

        return len(lastWord)
