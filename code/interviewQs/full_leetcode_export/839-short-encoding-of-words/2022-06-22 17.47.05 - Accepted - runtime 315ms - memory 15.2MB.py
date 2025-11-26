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

