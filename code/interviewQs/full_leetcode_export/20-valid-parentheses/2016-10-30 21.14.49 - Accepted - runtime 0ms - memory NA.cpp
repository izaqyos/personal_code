class Solution {
public:
    bool isValid(string s) {
        
        stack<char> stChar;
        for ( int i=0; i< s.length();++i)
        {
           // cout<<"at: "<<s[i]<<endl;
            if ( (s[i] == '(') || (s[i] == '[') || (s[i] == '{') )
            {
               // cout<<"push: "<<s[i] <<endl;
                stChar.push(s[i]);
            }
            else
            {
                if ( stChar.empty()) return false; //we have one of )]} w/o previous matching ([}
                else
                {
                    char c = stChar.top(); stChar.pop();
                    if ( ((c == '(') && (s[i] == ')')) || ( (c == '[') && (s[i] == ']') ) || ((c == '{') && (s[i] == '}'))  ) continue;
                    else return false;
                    
                }
                
            }
        }
        
        if (stChar.empty()) return true;
        else return false;
    }
};