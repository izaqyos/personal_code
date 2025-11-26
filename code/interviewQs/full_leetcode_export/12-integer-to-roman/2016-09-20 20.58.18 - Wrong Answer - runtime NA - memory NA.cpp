class Solution {
public:
    string intToRoman(int num) {
        
        /**
         I-1
         IV-4
         V-5
         IX- 9
         X-10
         XL-40
         L-50
         XC-90
         C-100
         CD-400
         D-500
         CM-900
         M-1000
         **/
         int d = 0;
         int decExp = 0; //decimal exponent
         string result;
         vector<string> onesConversion = { "I", "II", "III", "IV", "V", "VI", "VII", "VIII","IX", "X"};
         vector<string> tensConversion = { "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX","XC", "C"};
         vector<string> hundredsConversion = { "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC","CM", "M"};
         vector<string> thuasandsConversion = { "M", "MM", "MMM"};//max at 3999 no 4k
         
         while (num > 0)
         {
             d = num%10;
             
             if (decExp == 0)
             {
                 result.insert(0, onesConversion[d-1] );
             }
             else if (decExp == 1)
             {
                 result.insert(0, tensConversion[d-1] );
             }
             else if (decExp == 2)
             {
                 result.insert(0, hundredsConversion[d-1] );
             }
             else if (decExp == 3)
             {
                 result.insert(0, thuasandsConversion[d-1] );
             }
             
             decExp+=1;
             num/=10;
         }
         
         return result;
    }
};