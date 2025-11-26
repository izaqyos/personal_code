class Solution {
public:
    int myAtoi(string str) {
        
        if (str.empty() ) return 0;
        
        long long res = 0;
        int sign =1;
        for (auto c : str)
        {
            if (c == '-')
            {
                sign=-1;
                continue;
            }
            else if (c == '+') continue;
            
            int cint = (int)c;
            int cintNorm= cint-'0';
            cout<<"read char "<<c<<", val: "<<cint<<endl;
            if ( (0<=cintNorm) && (cintNorm<=10) )
            {
                res*=10;
                res+=cintNorm;
            }
            else 
            {
                return 0;
            }
        }
        return ( (res*sign < INT_MIN) || (res*sign > INT_MAX)) ? 0 : (res*sign) ;
      //return res*sign;
    }
};