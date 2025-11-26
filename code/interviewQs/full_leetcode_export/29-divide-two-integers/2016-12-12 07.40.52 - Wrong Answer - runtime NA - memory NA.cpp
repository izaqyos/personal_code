class Solution {
public:
    int badd(int a, int b)
    {
        int x,y;
        do
        {
            x = a^b; // add, no carries    
            y= a&b; //carries, need to shift left
            a=x;
            b=y<<1;
        } 
        while (y);
        
        return x;
    }
    
    int bneg(int a)
    {
        return badd(~a,1); //~a, 1s complemet. add 1 to make 2s complement which is the negative...
        
    }
    
    int bsub(int a, int b)
    {
        return badd(a,bneg(b));
    }
    
    
    int bmul(int x, int y)
    {
        int rmb =1;
        int res = 0;
        
        if (x<0) //negative won't work since all the left hand 1 bits are b/c of minus sign (2s complement)
        {
            x = bneg(x);
            y = bneg(y);
        }
        
        while (x>=rmb && y)
        {
            if (x & rmb) res = badd(y,res); // if rmb bit of x is 1 add y 
            rmb<<=1; // shift rmb 
            y<<=1; //shift y (mult by 2), also stop condition 
        }
        
        return res;
    }
    
    int bdiv(int a , int b)
    {
        int res = 0;
        
      //  cout<<"a: "<<hex<<a<<", INT_MAX: "<<hex<<INT_MAX<<", INT_MIN: "<<hex<<INT_MIN<<endl;
      
      cout<<"start"<<endl;
        if (b == 0) return INT_MAX;
       if (a  == INT_MIN && b == -1) return INT_MAX;  //abs(INT_MIN) = INT_MAX + 1
        
        int sign= ((a<0) ^(b<0)) ? -1:1;
        
        long long la = labs(a);
        long long lb = labs(b);
        
        /* can overflow for INT_MIN :(
        if (a<0) 
        {
            la= bneg(a);    
            sign ^=1; //flip once for -x
        }
        
           
       
         
        if (b<0)
        {
            lb = bneg(b);
            sign ^=1; //flip once for -y
        }
        */
        
       // cout<<"a: "<<a<<", |a|: "<<la<<", b: "<<b<<", |b|: "<<lb<<endl;
        while (la>=lb)
        {
            long long part=lb,mult=1;
            while (la >= (part<<1)) // so long a >= b*2^i , i - number of iterations
            {
                part<<=1; //part*=2
                mult<<=1; //mult*=2 
            }
            la-=part ;// a-=b*2^i
            res+=mult;// res+=2^i
            /* This works but too slow
            a = bsub(a,b);
            res++;
            */
        }
        
       // cout<<"sign: "<<sign<<", res: "<<res<<endl;
        if (sign) res = bneg(res);
        return res;
    }
    
    int divide(int dividend, int divisor) {
        return bdiv(dividend,  divisor);
    }
};