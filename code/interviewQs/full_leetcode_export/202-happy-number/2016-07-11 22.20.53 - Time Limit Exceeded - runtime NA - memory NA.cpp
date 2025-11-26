class Solution {
private:
    bool bprint = false;
    unsigned int imax = pow(10,5);
    
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
        
        // Fill map with "links" e.g. (1:1), (2:4),(3:9),(4:37) etc. 
        // Then for n, search in map link by link and if one of links is 1 return true;
        unordered_map<unsigned int,unsigned int> happys;
        unsigned int sqrDigSum = 0;
        for (unsigned int i=1; i<imax; ++i)
        {
           
            sqrDigSum = calcSqrDigSum(i);
            happys[i] = sqrDigSum;
          //  if(bprint) cout<<"i "<<i<<" happys[i]"<< happys[i] << endl;
        }
        
        int max_tries = 0;
        if (n<imax)
        {
            auto it = happys.find(n);
            while ((++max_tries)<imax)
            {
                if(bprint) cout<<"search loop. cur "<<(it->first)<<endl;
                
                 if (it == happys.end()) return false;
                 else if ( (it->second) == 1) return true;
                 else 
                 {
                     if(bprint) cout<<"new "<<(it->second);
                     it = happys.find( it->second);
                 }
            }
        }
        else
        {
            return false;
        }
        return false;
    }
};