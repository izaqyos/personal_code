class Solution {
public:
    int reverse(int x) {
        
        if ((-10<x) && (x<10)) return x;
        
        int sign = 1;
        if (x<0) sign = -1;
        x = x*sign; //positive, before ret repeat to return negative
        
        stack<int> st;
        int r=0;
        int q=0;
        int decM=1;//10^0 
        
        while (true)
        {
            
            q=x/10;
            r=x%10;
            st.push(r); 
            if (q == 0) break;
            
            x=q;
        }
        
        x=0;
        int d = 0;
        while (!st.empty())
        {
            d = st.top(); st.pop();
            x+= d*decM;
            decM*=10;
        }
        
        return x*sign;
    }
};