class Solution {
public:
    vector<string> generateParenthesis(int n) {
        unordered_set<string>  parenthCombSet;
        
        parenthCombSet = generateParenthesisRec(n);
    
        vector<string> vsRet(parenthCombSet.begin(), parenthCombSet.end());    
       // copy(parenthCombSet.begin(), parenthCombSet.end(), vsRet.begin());
        return vsRet;
    }
    
    unordered_set<string>  generateParenthesisRec(int n ) {
           /*
        Recursion approach
        
        0 -> {}
        1 -> { () }
        2 -> (1) & ()(1) & (1)() == { (()), ()() } // 2nd ()() duplicate
        3 -> (2) & ()(2) & (2)() == {((())), (()()), ()(()),()()(), (()))()} // 2nd ()()() duplicate
        */
        unordered_set<string> parenthCombSet;
     if (n <= 0) return parenthCombSet;
     if (n == 1) 
     {
         parenthCombSet.insert("()");
         return parenthCombSet;
     }
     if (n>1)
     {
         unordered_set<string> parenthInnerCombSet;
         parenthInnerCombSet = generateParenthesisRec(n-1);
         string leftBrace = "(";
         string rightBrace = ")";
         for (auto sParen : parenthInnerCombSet)
         {
             parenthCombSet.insert( sParen+leftBrace +rightBrace);
             parenthCombSet.insert( leftBrace+sParen+rightBrace);
             parenthCombSet.insert(leftBrace +rightBrace+sParen);
          
             
         }
             return parenthCombSet;
     }
         return parenthCombSet;
    }
};