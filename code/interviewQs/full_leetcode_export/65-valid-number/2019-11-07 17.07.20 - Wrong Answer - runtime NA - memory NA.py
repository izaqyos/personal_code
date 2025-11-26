from collections import defaultdict

class Solution:
    digits = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    sign_chars = {'-', '+' }
    other_chars = {'e', '.', }
    special_chars =  other_chars | sign_chars
    allowedChars = digits | special_chars
    def isNumber(self, inp):
        """
        idea, 
        a. trim spaces
        b. scan chars, compare w/ allowedChars dictionary {'0':True, ...
        ,'9':True, '-','e' ...
        c. For - . and e check if in allowed position (e.g. last char - is not
        number)
        """
        freqs = defaultdict(int)

        inp = inp.strip()
        if len(inp) == 0: #" "
            return False
        #print('testing stripped input ', inp)
        for index, char in enumerate(inp):
            freqs[char] = freqs[char]+1 
            #pdb.set_trace()
            if not char in self.allowedChars:
                return False
            if char == 'e':
                if index == 0 or index == len(inp)-1: #3e, e3
                    return False
                if (inp[index-1] not in self.digits) or  (( inp[index+1] not in self.digits) and (inp[index+1] != '-' )): #-e, e+ etc
                    return False
                postEindexscan = index +2
                while postEindexscan < len(inp):
                    if inp[postEindexscan] not in self.digits: #e-- e-+ etc
                        return False
                    postEindexscan = postEindexscan +1
            elif char == '.':
                if len(inp) == 1:
                    return False
                if (index > 0 and inp[index-1] in self.other_chars) or  ( index < len(inp)-1 and inp[index+1] not in self.digits): #e., .+
                    return False
            elif char == '-':
                if index != 0 and inp[index-1] != 'e' : #not one of -5, 4e-2
                    return False
                if inp[index+1] not in self.digits: #-+, -. -e etc
                    if inp[index+1] != '.':  #-. is  allowed 
                        return False
            elif char == '+':
                if index != 0: #+ is only valid at start
                    return False
                if inp[index+1] not in self.digits: #++, +e etc
                    if inp[index+1] != '.':  #+. is  allowed 
                        return False

        for c in self.special_chars:
            if freqs[c] > 1:
                return False
        return True
