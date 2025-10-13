#!/usr/bin/python

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

def main():
    words = ["", "ab", "cfd flga", "kdk dka ql  q", "          d        dwq          llfd        ", "                     ", "kkkkkkkkkkkkkkkkkkkkkkk"]
    sol = Solution()
    for word in words:
        print "got string [{0}]. Last word len={1}".format([word], sol.lengthOfLastWord(word))

if __name__ == "__main__":
    main()
