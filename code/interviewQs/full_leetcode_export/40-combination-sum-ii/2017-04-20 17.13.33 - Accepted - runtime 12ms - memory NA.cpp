class Solution {
public:

    void combinationSum2Rec(const vector<int>& candidates, int target, set<vector<int>> & Res, vector<int> & Comb, int currIdx)
    {
        if (target == 0) //means sum of numbers in Comb equals target
        {
            Res.insert(Comb);
            return;
        }
        
        for (int i = currIdx; ( (i < candidates.size() ) && (candidates[i] <= target)) ; ++i )
        {
            Comb.push_back(candidates[i]);
            combinationSum2Rec(candidates, target - candidates[i], Res, Comb, i+1); //no repeat allowed so recurse all permutations starting from i+1
            Comb.pop_back(); //important, at this point we're back from all permutations that include candidates[i] so remove it from Comb and proceed to candidates[i+1]
        }
        
        return; 
    }
    
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        
        set<vector<int>> Res; //use set to filter out duplicates
        vector<int> Comb; 
        
        sort(candidates.begin(), candidates.end());
        combinationSum2Rec(candidates, target, Res, Comb, 0);
        
        vector<vector<int>> vRes(Res.begin(), Res.end());
        return vRes;
    }
};