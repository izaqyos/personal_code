class Solution {
public:
    int romanToInt(string s) {
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
         int counter = 0;
         int i=0;
         while (  i<s.size())
         {
           //  cout<<"i: "<<i<<", size: "<<s.size()<<", char: "<<s[i]<<", count: "<<counter<<endl;
             if (s[i] == 'I')
             {
                 if( (i<s.size()-1) && (s[i+1] == 'V'))// IV
                 {
                     //cout<<"found 4"<<endl;
                     counter+=4;
                     i++;
                 }
                 else if( (i<s.size()-1) && (s[i+1] == 'X'))// IX
                 {
                     counter+=9;
                     i++;
                 }
                 else counter++;
             }
             else if (s[i] == 'V') counter+=5;
             
             else if (s[i] == 'X')
             {
                 if( (i<s.size()-1) && (s[i+1] == 'L'))// XL
                 {
                     counter+=40;
                     i++;
                 }
                 else if( (i<s.size()-1) && (s[i+1] == 'C'))// XC
                 {
                     counter+=90;
                     i++;
                 }
                 else counter+=10;
             }
             else if (s[i] == 'L') counter+=50;
             else if (s[i] == 'C')
             {
                 if( (i<s.size()-1) && (s[i+1] == 'D'))// CD
                 {
                     counter+=400;
                     i++;
                 }
                 else if( (i<s.size()-1) && (s[i+1] == 'M'))// CM
                 {
                     counter+=900;
                     i++;
                 }
                 else counter+=100;
             }
             else if (s[i] == 'D') counter+=500;
             else if (s[i] == 'M') counter+=1000;
             i++;
         }
         return counter;
    }
};