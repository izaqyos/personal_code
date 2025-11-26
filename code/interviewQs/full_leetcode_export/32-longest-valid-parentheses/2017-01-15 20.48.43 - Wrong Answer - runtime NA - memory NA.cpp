class Solution {
public:
    int longestValidParentheses(string s) {
        
        bool bDebug = false;
        stack<char> sOpen;
        int longest = 0;
        int currlen = 0;
        
        if (s.empty()) return 0;
        
        for (auto c : s)
        {
            if (bDebug) cout<<"processing "<<c<<endl;
            
            if ((c == '(') /** || (c == '[') || (c == '{') **/)
            {
                if (bDebug) cout<<"push "<<c<<endl;
                sOpen.push(c);
            }
            
            if ((c == ')') /** || (c == ']') || (c == '}') **/)
            {
                if ( ! sOpen.empty() )
                {
                    if (bDebug) cout<<"pop "<<c<<endl;
                    char ctop = sOpen.top();
                    //if ( ((ctop == '(') /** && (c == ')')) || ((ctop == '[]') && (c == ']'))  || ((ctop == '{') && (c == '}') **/ )  )
                    //{
                        currlen +=2;
                        
                        if (currlen > longest) longest = currlen;
                    //}
                    //else
                    //{
                    //    currlen = 0;
                    //}
                    sOpen.pop();
                }
                else 
                {
                    if (bDebug) cout<<"stack empty "<<endl;
                    currlen = 0;
                }
            }
        }
        
        return longest;
    }
};