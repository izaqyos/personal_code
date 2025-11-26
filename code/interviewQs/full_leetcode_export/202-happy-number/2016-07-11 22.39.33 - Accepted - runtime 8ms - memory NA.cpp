
class Solution {
private:
    bool bprint = false;

     //map to detect loops, mark every number we calculate. If we hit an existing one we have 
     // a circle so false for sure!
    unordered_map<unsigned int,unsigned int> happys;
public:
    unsigned int calcSqrDigSum(unsigned int n)
    {
        unsigned int mod = 0;
        unsigned int rem = n;
        unsigned int res = 0;
        while (rem > 0)
        {
           //if(bprint)  cout<<"divTen "<<divTen<<endl;
            
            mod = rem %10; // least significant digit
            res += mod*mod;
            rem/=10;
            
        }
        //if(bprint) cout<<"calcSqrDigSum of "<<n<<" is "<<res<<endl;
        return res;
    }
    
    bool isHappy(int n) {
        
        if (n <= 0) return false;
        
        if (happys.find( n ) != happys.end()) return false;
     
        happys[n] = 1;
        
        int next = calcSqrDigSum(n);
        if (next == 1) return true;
        else return isHappy(next);
    }
};
