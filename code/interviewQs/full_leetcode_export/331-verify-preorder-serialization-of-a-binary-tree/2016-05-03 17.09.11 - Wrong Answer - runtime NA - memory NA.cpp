class Solution {
public:
    bool isValidSerialization(string preorder) {
 
        // count max 2 # per num (node/leaf)
        unsigned int max_hash = 0;
        unsigned int nodes = 0;
        unsigned int idx = 0;
        if (  (0 <= (preorder[0] -'0') ) && ((preorder[0] -'0') <=9) )
        {
	    
            idx = 1;
            nodes = 1;
            max_hash = 2;

        
            while (idx < preorder.length())
            {	
                if (preorder[idx] == ',') 
                {
        
                    idx++;
		    continue;
                }
                else if (  (0 <= (preorder[idx] -'0') ) && ((preorder[idx] -'0') <=9) )
                {
        
                    max_hash++;
                    nodes++;
                }
                else if (preorder[idx] == '#') 
                {
        
                    max_hash--;
                }
                if ( (max_hash > nodes) && ((max_hash -nodes) > 1) ) return false; 
                
                idx++;
        
            }
            if (max_hash != 0 ) return false;
            
        }
        else
        {
	    
            return false;
        }
        return true;
    }
};

