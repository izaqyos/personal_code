class Solution:
    digits = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    sign_chars = {'-', '+' }
    special_chars = {'e', '.', } | sign_chars
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
        inp = inp.strip()
        #print('testing stripped input ', inp)
        for index, char in enumerate(inp):
            #pdb.set_trace()
            #print(char)
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
            elif char in self.sign_chars:
                if index == len(inp)-1:
                    return False
                if inp[index+1] in self.sign_chars: #--, -+, ++, +- etc
                    return False

        return True