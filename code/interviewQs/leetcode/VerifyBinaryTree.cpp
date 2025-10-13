#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Solution {
public:
    bool isValidSerialization(string preorder) {
 
        // count max 2 # per num (node/leaf)
        unsigned int max_hash = 0;
        unsigned int nodes = 0;
        unsigned int idx = 0;
        if (  (0 <= (preorder[0] -'0') ) && ((preorder[0] -'0') <=9) )
        {
	    cout<<"found valid root\n";
            idx = 1;
            nodes = 1;
            max_hash = 2;

            cout<<"Preloop Index: "<<idx<<", nodes: "<<nodes<<" max_hash: "<<max_hash<<" Str len "<<preorder.length()<<"\n";
            while (idx < preorder.length())
            {	
                if (preorder[idx] == ',') 
                {
                    cout<<"Found comma at index: "<<idx<<"\n";
                    idx++;
		    continue;
                }
                else if (  (0 <= (preorder[idx] -'0') ) && ((preorder[idx] -'0') <=9) )
                {
		    
                    cout<<"Found digit at index: "<<idx<<"\n";
		    while (preorder[idx] != ',') idx++; 
                    max_hash++;
                    nodes++;
                }
                else if (preorder[idx] == '#') 
                {
                    cout<<"Found hash at index: "<<idx<<"\n";
                    max_hash--;
                }
                if ( (max_hash > nodes) && ((max_hash -nodes) > 1) ) return false; 
                if ((max_hash == 0) && (idx < (preorder.length()-1)) ) return false; 
                
                idx++;
                cout<<"Inloop Index: "<<idx<<", nodes: "<<nodes<<"max_hash: "<<max_hash<<"\n";
            }
            if (max_hash != 0 ) return false;
            
        }
        else
        {
            if ( (preorder[idx] == '#') && preorder.length()==1) return true;
	    cout<<"Invalid tree (no valid root)\n";
            return false;
        }
        return true;
    }
};

int main()
{
	vector<string> vStrings;
	vStrings.push_back(string("9"));
	vStrings.push_back(string("9,#"));
	vStrings.push_back(string("9,#,#"));
	vStrings.push_back(string("9,#,92,#,#"));

	Solution sol;
	//for (vector<string>::const_iterator ci = vStrings.begin(); ci != vStrings.end(); ++ ci)
	for (auto ci : vStrings)
	{
	    bool isValid = sol.isValidSerialization(ci);
	    cout <<"String "<<ci<<" is "<< (isValid ? "valid": "not valid" )<<" representation of preorder traversal binary tree\n";
	}
}
