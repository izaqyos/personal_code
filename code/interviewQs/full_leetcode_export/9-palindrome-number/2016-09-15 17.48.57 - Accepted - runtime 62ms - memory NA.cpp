class Solution {
public:
    bool isPalindrome(int x) {
        
        if (x<0) return false;
        if ( (-10<x) && (x<10)) return true;
        
        stack<int> st;
        int xcpy = x;
        while (x!=0)
        {
            
            st.push(x%10);
           // cout<<"pushed: "<<x%10<<", x: "<<x<<endl;
            x/=10;
            
        }
        
        x = xcpy;
        
       // cout<<"st.size()/2: "<<st.size()/2<<endl;
       int runs =  st.size()/2;
        for (int i=0; i <= runs; ++i)
        {
            xcpy=st.top();
            st.pop();
            
            //cout<<"(i="<<i<<"), comapre st.top(): "<<xcpy<<", x tail: "<<x%10<<endl;
            
            if (! (xcpy== (x%10) ))
            {
                //cout<<"Found not pali"<<endl;
                return false;
            }
            x/=10;
        }
        
        return true;
    }
};