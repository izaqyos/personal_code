bool operator == (const vector<int> & v1, const vector<int> & v2)
        {
            if (v1.size() == v2.size())
            {
                for (int i=0; i<v1.size(); ++i)
                {
                    if (v1[i] != v2[i]) return false;
                }
            }
            else return false;
            
            return true;
        }


class Solution {
public:
        
    /*
    The simplest approach is as follows:

Sort the list: O(n lg n)
The sorted list is the first permutation
Repeatedly generate the "next" permutation from the previous one: O(n! * <complexity of finding next permutaion>)
Step 3 can be accomplished by defining the next permutation as the one that would appear directly after the current permutation if the list of permutations was sorted, e.g.:

1, 2, 2, 3
1, 2, 3, 2
1, 3, 2, 2
2, 1, 2, 3
2, 1, 3, 2
2, 2, 1, 3
...
Finding the next lexicographic permutation is O(n), and simple description is given on the Wikipedia page for permutation under the heading Generation in lexicographic order. If you are feeling ambitious, you can generate the next permutation in O(1) using plain changes


    Generation in lexicographic order[edit]
There are many ways to systematically generate all permutations of a given sequence.[49] One classical algorithm, which is both simple and flexible, is based on finding the next permutation in lexicographic ordering, if it exists. It can handle repeated values, for which case it generates the distinct multiset permutations each once. Even for ordinary permutations it is significantly more efficient than generating values for the Lehmer code in lexicographic order (possibly using the factorial number system) and converting those to permutations. To use it, one starts by sorting the sequence in (weakly) increasing order (which gives its lexicographically minimal permutation), and then repeats advancing to the next permutation as long as one is found. The method goes back to Narayana Pandita in 14th century India, and has been frequently rediscovered ever since.[50]

The following algorithm generates the next permutation lexicographically after a given permutation. It changes the given permutation in-place.

Find the largest index k such that a[k] < a[k + 1]. If no such index exists, the permutation is the last permutation.
Find the largest index l greater than k such that a[k] < a[l].
Swap the value of a[k] with that of a[l].
Reverse the sequence from a[k + 1] up to and including the final element a[n].
For example, given the sequence [1, 2, 3, 4] (which is in increasing order), and given that the index is zero-based, the steps are as follows:

Index k = 2, because 3 is placed at an index that satisfies condition of being the largest index that is still less than a[k + 1] which is 4.
Index l = 3, because 4 is the only value in the sequence that is greater than 3 in order to satisfy the condition a[k] < a[l].
The values of a[2] and a[3] are swapped to form the new sequence [1,2,4,3].
The sequence after k-index a[2] to the final element is reversed. Because only one value lies after this index (the 3), the sequence remains unchanged in this instance. Thus the lexicographic successor of the initial state is permuted: [1,2,4,3].
Following this algorithm, the next lexicographic permutation will be [1,3,2,4], and the 24th permutation will be [4,3,2,1] at which point a[k] < a[k + 1] does not exist, indicating that this is the last permutation.

    */
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> vres;
        
        if (n == 0) return vres;
        
        if (n == 1) 
        {
            vector<int> vint(1,nums[0]);
            vres.push_back(vint);
            return vres;
        }
        
        sort(nums.begin(), nums.end()); //1st permutation lexicographic order
        vres.push_back(nums);
        int k=n-1,l=0,j=0;
        while (k>0)
        {
           
            l=0;
                
                if (nums[k] > nums[k-1]) // we start k from up going down. find highest k such that cond. is met
                {
                    l=k;
                    j=l+1;
                    while (j<n)
                    {
                        if(nums[j] > nums[k-1]) l=j;
                        ++j;
                    } //here we find highest l, l>k-1 such that nums[l] > nums[k-1]
                    
                    //swap k-1 and l, then reverse order of nums[k] to nums[n-1]
                    swap(nums[k-1], nums[l]);
                    reverse(nums.begin()+k,nums.end());
                    vres.push_back(nums);  
                     k = n-1;
                    continue;
                }
                --k;
            
        }
        //if k==0, means nums is in reverse lexicographical order, this is last permutation 
       
        
        return vres;
    }
    /*
    // TLE rejected 
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        
        //use unordered_set<vector<int> > to save intermidate results
        // add to set first (so duplicated will not be added)
        //the from set add back to vres. need to pass hash function to set CTOR
        // the hash should run on vector<int> and used for =check
        //since anyway it is O(n), n being vec len its same complexity 
        
        int n = nums.size();
        vector<vector<int>> vres;
        
        if (n == 0) return vres;
        
        if (n == 1) 
        {
            vector<int> vint(1,nums[0]);
            vres.push_back(vint);
            return vres;
        }
        
        
        vector<int> nums_copy;
        vector<vector<int>> inter_res;
        
        struct hashF{
            size_t operator ()(const vector<int> & vec) const
            {
                size_t res = 0;
               
                for (int i=0; i<vec.size(); ++i)
                {
                    res+=(i+1)*vec[i];
                }
                return res;
            }
        };
        

        
        unordered_set<vector<int>, hashF> vecSet;
        
        for (int i=0; i<nums.size();++i)
        {
            nums_copy=nums;
            nums_copy.erase(nums_copy.begin()+i);
            inter_res = permuteUnique(nums_copy);
            for (auto & v : inter_res)
            {
                v.push_back(nums[i]);
                if ( vecSet.find(v) == vecSet.end())
                {
                    vecSet.insert(v);
                    vres.push_back(v);
                }
            }
        }
        
        return vres;
    }
 */
};