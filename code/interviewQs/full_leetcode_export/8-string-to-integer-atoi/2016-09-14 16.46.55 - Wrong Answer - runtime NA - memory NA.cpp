class Solution {
public:
    int myAtoi(string str) {
        
        if (str.empty() ) return 0;
        
        long long res = 0;
        int sign =1;
        bool signFound=false;
        bool procNum=false;
        for (auto c : str)
        {
            if (c == ' ') 
            {
                if (!procNum) continue;
                else break;
            }
            
            if ((!signFound) && (c == '-') )
            {
                if (!procNum) procNum=true;
                sign=-1;
                signFound=true;
                continue;
            }
            else if ((!signFound) && (c == '+'))
            {
                if (!procNum) procNum=true;
                signFound=true;
                continue;
            }
            else if ((signFound) && ( (c == '-') ||( c == '+') )  ) return 0;
            
            int cint = (int)c;
            int cintNorm= cint-'0';
          //  cout<<"read char "<<c<<", val: "<<cint<<endl;
            if ( (0<=cintNorm) && (cintNorm<=10) )
            {
                if (!procNum) procNum=true;
                res*=10;
                res+=cintNorm;
               // cout<<"res: "<<res<<endl;
            }
            else 
            {
                break;
            }
        }
       // cout<<"res: "<<res<<", sign: "<<sign<<endl;
        if (res*sign < INT_MIN) return INT_MIN;
        else if (res*sign > INT_MAX) return INT_MAX;
        else return (res*sign) ;
      //return res*sign;
    }
};