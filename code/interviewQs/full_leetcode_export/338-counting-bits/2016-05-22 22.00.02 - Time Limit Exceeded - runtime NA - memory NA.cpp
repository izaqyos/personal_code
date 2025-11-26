class Solution {
public:
    vector<int> countBits(int num) {
     
     vector<int> vRet(num);
     if (num == 0)
     {
         vRet[0] = 0;
         return vRet;
     }
         vRet[0] = 0;
         vRet[1] = 1;
     
     int prevExp=0; // 2^0 - 1
     int k=pow(2,prevExp+1);
     while (k <=  num)
     {
    
             if ( ( k < pow(2,prevExp+1) + ((pow(2,prevExp+2)-pow(2,prevExp+1))/2)  ) )//2,4-5,8-11 etc
             {
                 vRet[k] = vRet[pow(2,prevExp) + (k-pow(2,prevExp+1))]; //copy 1 bit count of prev group
             }
             else if (k < pow(2,prevExp+2))
             {
                 vRet[k] = vRet[pow(2,prevExp) + (k - ((pow(2,prevExp+2)-pow(2,prevExp+1))/2)  )] +1; //copy 1 bit count of prev group and add one to each bit
             }
             else if (k == pow(2,prevExp+2)) prevExp++;
         
     }
     
     return vRet;
    }
};