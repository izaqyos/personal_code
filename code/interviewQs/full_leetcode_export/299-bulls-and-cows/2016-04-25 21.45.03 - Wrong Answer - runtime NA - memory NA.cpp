class Solution {
public:
    string getHint(string secret, string guess) {
        unsigned int freqs [10] = {0};
        unsigned int bulls = 0;
        unsigned int cows = 0;
        for (string::const_iterator cit = secret.begin() ; cit!= secret.end(); ++cit)
        {
            freqs[ (*cit) - '0']++;
        }
        
        for (unsigned int i = 0; i<secret.size(); ++i)
        {
            if (secret[i] == guess[i]) bulls++;
            else if ( freqs[ guess[i] - '0'] > 0 )
            {
                cows++;
                freqs[ guess[i] - '0'] -- ;
            }
            
        }
        string res = std::to_string(bulls);
        res += "A";
        res += std::to_string(cows);
        res += "B";
        return res;
    }
};