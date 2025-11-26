class Solution {
public:
    int superPow(int a, vector<int>& b) {
     if (b.empty() || ((b.size() == 1)&&(b[0]==0)) ) return 1;
     if ((b.size() == 1)&&(b[0]==1)) return a;
     
     int res = 1;
     
     
     long long bNum = 0;
     for ( auto it = b.begin(); it != b.end(); ++it)
     {
         if (it == b.begin()) bNum=*it;
         else
         {
            bNum *= 10;
            bNum+= *it;
         }
     }
     
     for (int i=0; i<bNum; ++i) res= (a*res)%1337;
     
     return res;
    }
};