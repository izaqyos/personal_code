class Solution {
public:
    string multiply(string num1, string num2) {
        bool bD = false;
    
        if (num1.empty() || num2.empty()) return "0";
        
        int ires=0, carry=0;
        string res="";
        vector<int> vres(num1.size()+num2.size(),0);
        
        int insertI = 0;
        for(int i=num1.size()-1;i>=0;--i) //since nums are stored as strings smallest digits are on right side
        {
            carry = 0;
            for(int j=num2.size()-1;j>=0;--j)
            {
                if (bD) cout<<"multiply num1["<<i<<"]*num2["<<j<<"]="<<(num1[i]-'0')*(num2[j]-'0')<<endl;
                
                insertI = num1.size() - (i+1) + num2.size() - (j+1) ; //insert digits to slots 0,1,... 
                vres[insertI] += carry + (num1[i]-'0')*(num2[j]-'0'); // add previous carry + current digits mult res
                carry = vres[insertI]/10; // calc new carry
                vres[insertI] = vres[insertI]%10; //calc new res digit val
                if (bD) cout<<"vres["<<insertI<<"]="<<vres[insertI]<<", carry="<<carry<<endl;
            }
            vres[num1.size() - (i+1) + num2.size()] +=carry;    //last carry spills to next digit 
        }
        
        
        if (bD) cout<<"vres["<<vres.size()-1<<"]="<<vres[vres.size()-1]<<endl;
        
        if (bD) for (auto n : vres) cout<<n;
        
        bool skipLeadingZeros = true;
        for (int i=vres.size()-1; i >=0;--i)
        {
            
            if (skipLeadingZeros )
            {
                if (vres[i] > 0) 
                    {
                        skipLeadingZeros = false;
                        res+= vres[i]+'0';
                    }
            }
            else
            {
                res+= vres[i]+'0';
            }
        
        }
        
        return res.empty()?"0" : res;
    }
};