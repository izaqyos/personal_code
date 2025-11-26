class Solution {
public:
    int integerBreak(int n) {
        int mem[3] = {0,0,0} ; // how many 1,2,3 we have factored
        if (n == 2) return 1;
        else if (n>2)
        {
            mem[0]=2; // two 1s
            mem[1]=0; // zero 2
            mem[2]=0; // zero 3
            for (int i=3; i<=n;++i)
            {
                if (mem[0]>0) // we have 1s
                {
                    mem[0]--;
                    mem[1]++; //pass from 1 to 2
                }
                else if (mem[1]>0) //we have 2s
                {
                    mem[1]--;
                    mem[2]++; //pass from 2 to 3
                }
                else if (mem[1]==0) // zero 2s, so all 3s one of which +1 is two 2s, so add two 2s substract one 3
                {
                    mem[1]+=2;
                    mem[2]--;
                }
                
                
            }
        }
        return ( pow(2,mem[1]) * pow(3,mem[2]) );
    }
};