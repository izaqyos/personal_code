//check if works...
class Solution {
public:
    bool isNumber(string s) {
        int i = 0, j = (int)(s.size()) - 1;  // remove space;
        while(i <= j && s[i] == ' ') i++;
        while(j >= i && s[j] == ' ') j--;
        bool seen_e = false, seen_sign = false, seen_digit = false, seen_dot = false;
        for(int k = i; k <= j; k ++){
            if (isdigit(s[k])){
                seen_digit = true;
            } else if (s[k] == '-' || s[k] == '+'){
                if (seen_sign || seen_digit || seen_dot) return false;
                seen_sign = true;
            } else if (s[k] == '.'){
                if (seen_dot || seen_e) return false;
                seen_dot = true;
            } else if (s[k] == 'e'){
                if (seen_e || !seen_digit) return false;
                seen_e = true;
                seen_sign = seen_digit = seen_dot = false;
            } else {
                return false;
            }
        }
        return seen_digit;
    }
};