#include <iostream>
#include <vector>

using namespace std;


class Solution {
public:
    vector<int> largestDivisibleSubset(vector<int>& nums) {
        if (nums.empty() ||(nums.size()==1)) return nums;
        
        vector<int>  vLDS_biggest; // vLDS_biggest[i] will contain size of largestDivisibleSubset "ending" w/ nums[i]
        
        sort(nums.begin(), nums.end()); 
        
        vLDS_biggest.push_back(1); // size of largestDivisibleSubset "ending" w/ nums[0], which is smallest num
        int longest = 0;
        int longestIdx = 0;
        vector< vector <int> > longestSubsetPerIdx;
        
        vector<int> vecInt;
        vecInt.push_back(nums[0]);
        longestSubsetPerIdx.push_back(vecInt);//at 0 -> {nums[0]}
        
        for (int i=1; i < nums.size(); ++i)
        {
            cout<<"calc i "<<i<<endl;
            longest =0;
            longestIdx = 0;
            
            for (int j=i-1; j>=0; --j)
            {
                cout<<"calc j "<<j<<"Test mod "<<nums[i]<<"%"<<nums[j]<<endl;
                if ((nums[i] %  nums[j]) == 0)    
                {
                    if (vLDS_biggest[j] > longest)
                    {
                        longest = vLDS_biggest[j];
                        longestIdx = j;
                       cout<<"longest: "<<longest<<", + index: "<<longestIdx<<endl;
                    }
                }
            }
            if (longest == 0 ) // nums [i] doesn't divide by any of nums[0...i-1]
            {
                cout<<"num "<<nums[i]<<" doesn't divide by any of nums[0..."<<i-1<<"]\n";
                vLDS_biggest[i] = 1; // just divide by himself
                vector<int> set;
                set.push_back(nums[i]);
                longestSubsetPerIdx.push_back(set);
            }
            else
            {
                cout<<"num "<<(nums[i])<<" divides LDS size "<<longest<<"ending w "<<(nums[longestIdx])<<endl;
                vLDS_biggest[i] = longest+1; //  divides a longer (the longest) seq...
                vector<int> set = longestSubsetPerIdx[longestIdx];
                set.push_back(nums[i]);
                longestSubsetPerIdx.push_back(set);
            }
            cout<<"longestSubsetPerIdx size "<<longestSubsetPerIdx.size()<<endl;
            
        }
        
        cout<<"longestSubsetPerIdx size "<<longestSubsetPerIdx.size()<<", LDS index "<<nums.size()-1<<endl;
        for (int i = 0; i< longestSubsetPerIdx.size();++i)
        {
            cout<<"longestSubsetPerIdx set "<<i<<endl<<"{";
            for (auto j :longestSubsetPerIdx[i] )
            {
                cout<<j<<",";
            }
            cout<<"}"<<endl;
        }
        cout<<"aaa"<<endl;
        vector<int> vRet = longestSubsetPerIdx[nums.size()-1];
        cout<<"bbb"<<endl;
        return vRet;
        
    }
};

int main()
{
	int numar[7] = {2,3,5,7,11,13,17};
	vector<int> vinp(numar, numar +7);
	vector<int> vret;

	Solution sol;
	vret = sol.largestDivisibleSubset(vinp);
	cout<<"res: {";
	for (auto n: vret)
	{
		cout<<n;

	}
	cout<<"}"<<endl;
	return 1;
}
