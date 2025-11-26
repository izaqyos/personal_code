class Solution {
public:
    int reverse(int x) {
        if (10<x && x<10) return x;
        //int sign = (x<0) ? -1 : 1;
        
        long long res = 0;
        int dec = 1;
        while ( x != 0)
        {
            res*=10;
            res += (x%10);
            
            x /=10;
            
            
           // cout<<"res: "<<res<<", x:"<<x<<endl;
        }
        
        return ((res<INT_MIN) || (res>INT_MAX)) ? 0 : res;
    }
};