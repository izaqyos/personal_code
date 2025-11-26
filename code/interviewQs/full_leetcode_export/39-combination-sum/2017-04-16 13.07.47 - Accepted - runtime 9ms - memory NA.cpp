class Solution {
public:

    // recurse as follows.
    // start from cur, try to add candidates[cur] if candidates[cur] <= target, if so add to comb. 
    // set target = target - candidates[cur] and recurse call combinationSumRec(candidates, res, comb, target, cur)
    //stop condition when target == 0
    void combinationSumRec(const vector<int> & candidates, vector<vector<int>> & res, vector<int> & comb, int target, int cur)
    {
        if(target == 0)
        {
            res.push_back(comb);
            return;
        }
        
        
        for (int i=cur; i<candidates.size() && (candidates[i] <=target) ; ++i)
        {
            comb.push_back(candidates[i]);
            combinationSumRec(candidates, res, comb, target-candidates[i] , i); 
            comb.pop_back();
        }
    }
    
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
     
     vector<vector<int>> res;
     vector<int> comb;
     sort(candidates.begin(), candidates.end());
     combinationSumRec(candidates, res, comb, target, 0); 
     return res;
     
    }
    
};