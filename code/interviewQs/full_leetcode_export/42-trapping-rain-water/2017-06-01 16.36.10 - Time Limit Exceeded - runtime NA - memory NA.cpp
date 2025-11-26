class Solution {
public:
    int trap(vector<int>& height) {
        bool bd = false;
        //idea
        // process line by line. e.g.
        // first iteration, check for >0,0,>0 seq. each one holds 1 water, sum all 1s
        // then for each n>0, n-- , (optimization: delete leading and trailing 0s) , repeat  check for >0,0,>0 seq. each one holds 1 water, sum all 1s
        // complexity o(n*k) where k is biggest num
        
        int li=-1,ri=-1; // left and right indices
        int res = 0;
        
        if (height.empty()) return res;
        
        do 
        {
            if (bd) cout<<"list size: "<<height.size()<<endl;
            //trim leading & trailing zeros
            while ((!height.empty()) && height[0] == 0) 
            {   
                if (bd) cout<<"Erasing leading 0 element"<<endl;
                height.erase(height.begin());
            }
            while ((!height.empty()) && height[height.size()-1] == 0) 
            {
                if (bd) cout<<"Erasing trailing 0 element"<<endl;
                height.erase(height.begin() +height.size()-1);
            }
                
            
            
            if (height.empty()) 
            {
                if (bd) cout<<"List is empty. breaking loop"<<endl;
                break;
            }
            li=-1,ri=-1;
            
            int i=0;
            
            for (;i<height.size();++i)
            {
                if ( (li== -1) && height[i]>0 ) li=i;
                else if (li>=0)  
                {
                    //if ( height[i] ==0 ) // do nothing
                    
                    if ( height[i] >0 ) //check for trapped water
                    {
                        ri=i;
                        if (ri > li+1) //when ri == li+1 li and ri have no space to capture water
                        {
                            //add ri-li to trapped water container
                            res += ri-li-1;
                        }
                        
                        li=ri; //advance li and reset ri
                        ri = -1;
                    }
                }
            }
            for (auto & n : height) {if (n>0) n--;}   //reduce all values by 1, e.g. remove lowest level
            
            
        }
        while (! height.empty());
        
        return res;
    }
};