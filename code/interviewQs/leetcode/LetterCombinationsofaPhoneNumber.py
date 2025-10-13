class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        digitsLetters = dict({'2':'abc', '3':'def', '4':'ghi', '5':'jkl', '6':'mno', '7':'pqrs', '8':'tuv', '9':'wxyz'})
        ret = []
        for d in digits:
            if not ret:
                ret = [_ for _ in digitsLetters[d]]
            else:
                newret = []
                for retelem in ret:
                    for appendchar in digitsLetters[d]:
                        newret.append(retelem + appendchar) 
                ret = newret
        return ret

"""
Solutions from leet:

1. python recursion 
   def letterCombinations(self, digits: str) -> List[str]:
        dictionary = {
            '2': list(map(chr,range(ord('a'),ord('d')))),
            '3': list(map(chr,range(ord('d'),ord('g')))),
            '4': list(map(chr,range(ord('g'),ord('j')))),
            '5': list(map(chr,range(ord('j'),ord('m')))),
            '6': list(map(chr,range(ord('m'),ord('p')))),
            '7': list(map(chr,range(ord('p'),ord('t')))),
            '8': list(map(chr,range(ord('t'),ord('w')))),
            '9': list(map(chr,range(ord('w'),ord('z')+1))),
        }
        result = []
        if len(digits) == 0:
            return result
        def recurse(curr,k,digits):
            if len(curr) == len(digits):
                result.append(curr)
                return 
            for i in digits[k]:
                for j in dictionary[i]:
                    recurse(curr+j,k+1,digits)            
            
        recurse("",0,digits)
        return result

2. c++ recursion 
class Solution {

private:
void solve(string digit, string output, int index, vector <string> &ans,  string mapping[]){
    
    //base Case
    if(index >=  digit.length()){
        ans.push_back(output);
        return ;
    }
    
    int number = digit[index] - '0';
    
    string value = mapping [number];
    
    for(int i =0; i<value.length(); i++){
        output.push_back(value[i]);
        
        solve(digit, output, index+1, ans, mapping);
        output.pop_back();
    }
}
public:
vector letterCombinations(string digits) {
vectorans;
if(digits.length()== 0)
return ans;

    string output ="";
    int index = 0;
    
    string mapping [10] = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    
    solve(digits,output, index, ans,mapping);
    
    return ans;
    
}
};

3. excellent explanation 

https://leetcode.com/problems/letter-combinations-of-a-phone-number/discuss/2021106/Java-4-Approaches%3A-BF-4-Loops-Backtracking-BFS-Queue-with-Image-Explaination
"""
