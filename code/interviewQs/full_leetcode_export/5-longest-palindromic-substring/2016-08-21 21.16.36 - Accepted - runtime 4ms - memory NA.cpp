class Solution {
public:
    string longestPalindrome(string s) {
   
   if (s.size() <=1) return s;
   
   int start = 0;
   int left,right;
   int leftmost=0;
   int max_len=1;
   int str_len=s.size();
   while (start < s.size() && ((str_len-start)>max_len/2) ) //if len-start (what's left) <= max found pali /2 no chance to find longer pali
   {
       left=right=start;
       
       while(right<str_len-1 && ( s[right] == s[right+1])) //eat same char
       {
           right++;
       }
       start = right+1; //either next char, or we ate many same char
       while (left>0 && right<str_len-1 && s[left-1] == s[right+1]) //expand pali to left and right
       {
           left--;
           right++;
       }
       
       if (max_len <(right-left+1))
       {
           max_len = right-left+1;
           leftmost = left; //for later returning longest found pali
       }
       
       
   }
   return s.substr(leftmost, max_len);
    }
};