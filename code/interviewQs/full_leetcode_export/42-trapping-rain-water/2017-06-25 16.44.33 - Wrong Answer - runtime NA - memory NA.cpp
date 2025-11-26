 class Solution {
public:
    int trap(vector<int>& height) {
        bool bd = false;
        
        //2nd idea
        // scan from left to right. init left, min and right markers. 
        // loop height
        // left <- first n>0 at pos i, m<-l
        // if left set, if h[i] >l (== h[i-1]) then l<-h[i]
        // else set flag Ascending<-false, 
        // if h[i] <m , m<-h[i]
        // for first h[i] > h[i-1] set Ascending<-true , r<-h[i]
        // if Ascending and h[i]>h[i-1] set r<-h[i]
        // Then, so long as a. h[i] < n, add b. h[i-1]>=h[i] continue
        // if h[i] >=n or h[i]>h[i-1] or i==h.size()-1 and left is set then set right to i
        // now push l,r to vp ( vector<pair<int, int>> )
        // all this o(n)
        // next iterate over vp. for each pair run from l+1 to r, and add res+=min(l,r)-h[j]
        // complexity o(n)
        
        int li=-1,ri=-1; // left and right indices
        int res = 0;
        
        if (height.empty()) return res;
        
        int n=height.size();
        vector<pair<int,int>> vp; 
        bool bFoundDescending = true;
        
        int i = 0;
        while (i < height.size()-1)
        {
            if (bd) cout<<"i="<<i<<", li="<<li<<", ri="<<ri<<endl;
            if  (li == -1) 
            {
                if (height[i]>0) 
                {
                    while (height[i] <= height[i+1]) ++i; //skip vals until reaching left most peak
                    li = i;
                    if (bd) cout<<"set li="<<li<<endl;
                }
            }
            else // (li>=0) 
            {
                if (bd) cout<<"li="<<li<<", now look for ri..."<<endl;
                while (height[i] > height[i+1]) // skip desending vals
                {
                    ++i;
                }
                if (bd) cout<<"last descending index="<<i<<endl;
                while ((i<height.size()-1) && (height[i] <= height[i+1]) ) 
		{
			i=i+1; //skip vals until reaching right most peak
			if (bd) cout<<"advanced i to "<<i<<", height size="<<height.size()<<endl;
		}
                if (bd) cout<<"last ascending index="<<i<<endl;
                if (i == height.size()) break;
                //at this point we have valid li and valid ri, add water
                ri = i;
                if (bd) cout<<"pushing indices: li="<<li<<", ri="<<ri<<endl;
                if ((li<ri-1) && (ri<height.size())) vp.push_back(make_pair(li,ri));
                li=ri;
                ri=-1;
            }
            ++i;
        }
                //here loop over vp left and right pairs, add to res min(l,r) - h[i]
        for (auto pair : vp)
        {
            int m = min(height[pair.first], height[pair.second]);
            for (int i = pair.first +1; i< pair.second; ++i)
            {
                res+=max(m-height[i], 0);//only take positive amount
            }
        }
        
        return res;

    }
};