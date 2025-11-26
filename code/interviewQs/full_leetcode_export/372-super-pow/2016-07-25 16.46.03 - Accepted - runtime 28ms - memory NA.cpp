class Solution {
public:
    int superPow(int a, vector<int>& b) {
     int nMod = 1337;
     if (b.empty() || ((b.size() == 1)&&(b[0]==0)) ) return 1;
     if ((b.size() == 1)&&(b[0]==1)) return a%nMod;
     
     int res = 1;
     int apow10 = a%nMod; // init to a*10^0
     
     reverse(b.begin(),b.end()); // run from least to most important, each time multiply by 10**i 0<=i<b.size()
     
     for (int i=0; i<b.size(); ++i)
     {
        for (int j=0; j<b[i];++j)// multiply a j times
        {
            res =   ((res%nMod)*(apow10%nMod))%nMod;
        }
        
        int temp = apow10; // for each iteration through b apow10 should be a*10^i so multiply apow10 10 times
        for (int k=0; k<9;++k) temp = ((temp%nMod)*(apow10%nMod))%nMod;
        apow10 = temp; 
     }
     
     return res;
    }
};