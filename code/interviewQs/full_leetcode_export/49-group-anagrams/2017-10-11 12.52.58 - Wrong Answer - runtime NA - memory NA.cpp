class Solution {
public:
    int calcHash(string & str)
    {
        //write small python script to gen first 26 prime nums
        //[yizaq@YIZAQ-M-W1ZV:Mon Sep 18:~/Desktop/Work/code/python/simple:]$ ./simplestPrimeSieve.py 
 //generate how many primes ?22
//[2, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43]
//{a , 2},{  b, 3 },{  c, 5 },{  d, 7 },{  e, 9 },{  f, 11 },{  g, 13 },{  h, 15 },{  i, 17 },{  j, 19 },{  k, 21 },{  l, 23 },{  m, 25 },{  n, 27 },{  o, 29 },{  p, 31 },{  q, 33 },{  r, 35 },{  s, 37 },{  t, 39 },{  u, 41 },{  v, 43 },{  w, 45 },{  x, 47 },{  y, 49 },{  z, 51 }
        vector<pair<char,int>> chars = { {'a' , 2},{  'b', 3 },{  'c', 5 },{  'd', 7 },{  'e', 9 },{  'f', 11 },{  'g', 13 },{  'h', 15 },{  'i', 17 },{  'j', 19 },{  'k', 21 },{  'l', 23 },{  'm', 25 },{  'n', 27 },{  'o', 29 },{  'p', 31 },{  'q', 33 },{  'r', 35 },{  's', 37 },{  't', 39 },{  'u', 41 },{  'v', 43 },{  'w', 45 },{  'x', 47 },{  'y', 49 },{  'z', 51 }  };
        
        int hash = 1;
        for (auto c: str)
        {
            hash*=chars[c-'a'].second;
        }
        
        return hash;
    }
    
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
      
        //my idea, create a map<int , vector<string>> 
        // int is a hash of the word, which is same for all anagrams.
        // how to calculate, each letter a-z is assigned a prime #. 2,3,5 etc.
        // then for each word calculate letter product. guarenteed same for anagrams.
        // push back to map[hash]
        // last copy to vector of vectorys
        
    
    unordered_map<int, vector<string>> Anagrams;
        vector<vector<string>> res;
        for (auto s : strs)
        {    
            Anagrams[calcHash(s)].push_back(s);
        }
        
        for (auto kv : Anagrams)
        {
            res.push_back(kv.second);
        }
        
        return res;
    }
};