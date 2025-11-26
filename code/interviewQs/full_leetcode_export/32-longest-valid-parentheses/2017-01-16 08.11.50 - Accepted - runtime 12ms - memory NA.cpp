class Solution {
public:
    int longestValidParentheses(string s) {
        
        bool bDebug = false;
        stack<int> sOpen;//hold index of closest '('
        int longest = 0;
        
        
        if (s.empty()) return 0;
        
        for (int i=0; i<s.length();++i)
        {
            if (bDebug) cout<<"processing s["<<i<<"]="<<s[i]<<endl;
            
            if ((s[i] == '(') /** || (c == '[') || (c == '{') **/)
            {
                if (bDebug) cout<<"push "<<i<<endl;
                sOpen.push(i);
            }
            
            if ((s[i] == ')') /** || (c == ']') || (c == '}') **/)
            {
                if ( ! sOpen.empty()  && (s[sOpen.top()] == '('))
                {
                        if (bDebug) cout<<"pop "<<i<<endl;
                        sOpen.pop();
                }
                else 
                {
                    if (bDebug) cout<<"stack empty or mismatch parenthesis, push "<<i<<endl;
                    sOpen.push(i);
                }
            }
        }
        
        if (sOpen.empty()) return s.length();
        else 
        {
            
            int preSeq = 0, postSeq = s.length() ;
            while (!sOpen.empty())
            {
                preSeq = sOpen.top(); //right most position that doesn't have match, so from right end to preSeq+1 we have match
                longest = max (longest, postSeq-preSeq-1);
                sOpen.pop();
                postSeq = preSeq;
            }
            longest = max(longest, postSeq); //postSeq is last preSeq so another valid match is from 0 to last preSeq
        }
        
        return longest;
    }
};