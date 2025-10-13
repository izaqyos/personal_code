""" 
A valid encoding of an array of words is any reference string s and array of indices indices such that:

words.length == indices.length
The reference string s ends with the '#' character.
For each index indices[i], the substring of s starting from indices[i] and up to (but not including) the next '#' character is equal to words[i].
Given an array of words, return the length of the shortest reference string s possible of any valid encoding of words.

 

Example 1:

Input: words = ["time", "me", "bell"]
Output: 10
Explanation: A valid encoding would be s = "time#bell#" and indices = [0, 2, 5].
words[0] = "time", the substring of s starting from indices[0] = 0 to the next '#' is underlined in "time#bell#"
words[1] = "me", the substring of s starting from indices[1] = 2 to the next '#' is underlined in "time#bell#"
words[2] = "bell", the substring of s starting from indices[2] = 5 to the next '#' is underlined in "time#bell#"
Example 2:

Input: words = ["t"]
Output: 2
Explanation: A valid encoding would be s = "t#" and indices = [0].
 

Constraints:

1 <= words.length <= 2000
1 <= words[i].length <= 7
words[i] consists of only lowercase letters.
"""

""" 
idea.
a. one pass over words build dictonary for word of all of it's suffixed to it. 
e.g.
time would yeild, {'time':'time','ime':'time', 'me':'time', 'e':'time'}  
then on second pass we remove from words any word who's value length in suffixes dictonary is greater than it.
e.g. 'me' length 2 < 'time' lenght 4
we done sum length of words + (#words -1) for the # seprator
"""
class Solution:
    def minimumLengthEncoding(self, words: List[str]) -> int:
        suffixes = dict()
        #remove duplicates 
        words_set=set(words)
        words = list(words_set)
        for word in words:
            if not word in suffixes:
                i = 0
                while i<len(word):
                    if word[i:] in suffixes: #replace shorter words with longer ones. ex. we had 'me':'me' and now processing 'time' so replace to 'me':'time'
                        if  len(word) > len(suffixes[word[i:]]):
                            suffixes[word[i:]]  = word
                    else:
                        suffixes[word[i:]] =word
                    i+=1

        #longest_words = [] #we don't really need the actual encoding string. just it's length
        encoding_str_len = 0
        for word in words:
            if len(word) == len(suffixes[word]):
                #longest_words.append(word)
                encoding_str_len+=len(word)+1 #+1 for hash
        #encoding_str='#'.join(longest_words)
        return encoding_str_len

