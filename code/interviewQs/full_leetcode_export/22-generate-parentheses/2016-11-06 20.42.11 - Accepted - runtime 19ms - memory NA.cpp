class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> vsRet;
        
        generateParenthesisRec(vsRet, "", n, 0);
        
        return vsRet;
    }
    
    void  generateParenthesisRec(vector<string> & vsRet, string s, int r, int l ) {
        cout<<"Called with s: "<<s<<", r: "<<r<<", l: "<<l<<endl;
           /*
        Recursion approach
        
        n = r + l - r: number of possible '(', l : number of possible ')''
        
        stop: both r and l equal zero. push s int vsRet
        if r>0 add '( , r<-r-1 and l<-l+1 (since we removed '(' and we need reserve another ')' )
        
        if l>0 add ')' and call w/ r and l-1  (since we removed ')')
        */
        
     if ((r== 0)&&(l==0)) 
     {
         cout<<"Add final: "<<s<<endl;
         vsRet.push_back(s);
         return;
     }
     
    
     if (r>0)
     {
      
         generateParenthesisRec(vsRet, s+"(", r-1,l+1);
     }
     
      if (l>0)
     {
    
         generateParenthesisRec(vsRet, s+")", r,l-1);
     }
     
    }
};