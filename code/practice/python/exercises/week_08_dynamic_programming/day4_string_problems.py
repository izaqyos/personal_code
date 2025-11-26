"""
Week 8, Day 4: String DP Problems

Learning Objectives:
- Master LCS and LIS variations
- Learn palindrome problems
- Practice string matching
- Understand edit distance variations
- Solve complex string problems

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: Longest Palindromic Substring
# ============================================================

def longest_palindrome_substring():
    """
    Find longest palindromic substring.
    
    Palindrome: Reads same forwards and backwards
    """
    print("--- Exercise 1: Longest Palindromic Substring ---")
    
    def longest_palindrome(s):
        """DP approach - O(n²)"""
        n = len(s)
        if n < 2:
            return s
        
        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1
        
        # Single characters are palindromes
        for i in range(n):
            dp[i][i] = True
        
        # Check substrings of length 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start, max_len = i, 2
        
        # Check substrings of length 3+
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    start, max_len = i, length
        
        return s[start:start + max_len]
    
    def expand_around_center(s):
        """Expand around center - O(n²) time, O(1) space"""
        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1
        
        start, max_len = 0, 0
        for i in range(len(s)):
            len1 = expand(i, i)      # Odd length
            len2 = expand(i, i + 1)  # Even length
            length = max(len1, len2)
            
            if length > max_len:
                max_len = length
                start = i - (length - 1) // 2
        
        return s[start:start + max_len]
    
    test_cases = ["babad", "cbbd", "racecar"]
    
    for s in test_cases:
        result = longest_palindrome(s)
        print(f"String: '{s}'")
        print(f"  Longest palindrome: '{result}'\n")
    
    print()

# ============================================================
# EXERCISE 2: Palindromic Substrings Count
# ============================================================

def count_palindromic_substrings():
    """
    Count all palindromic substrings.
    
    TODO: Count instead of find
    """
    print("--- Exercise 2: Count Palindromic Substrings ---")
    
    def count_substrings(s):
        """Count palindromic substrings"""
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0
        
        # Single characters
        for i in range(n):
            dp[i][i] = True
            count += 1
        
        # Length 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                count += 1
        
        # Length 3+
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    count += 1
        
        return count
    
    test_cases = ["abc", "aaa", "racecar"]
    
    for s in test_cases:
        count = count_substrings(s)
        print(f"String: '{s}'")
        print(f"  Palindromic substrings: {count}\n")
    
    print()

# ============================================================
# EXERCISE 3: Longest Common Substring
# ============================================================

def longest_common_substring():
    """
    Find longest common substring (contiguous).
    
    TODO: Different from subsequence
    """
    print("--- Exercise 3: Longest Common Substring ---")
    
    def lc_substring(text1, text2):
        """Longest common substring"""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_len = 0
        end_pos = 0
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    if dp[i][j] > max_len:
                        max_len = dp[i][j]
                        end_pos = i
                else:
                    dp[i][j] = 0  # Must be contiguous
        
        return text1[end_pos - max_len:end_pos]
    
    test_cases = [
        ("abcde", "abfce"),
        ("ABABC", "BABCA"),
        ("GeeksforGeeks", "GeeksQuiz")
    ]
    
    for text1, text2 in test_cases:
        substring = lc_substring(text1, text2)
        print(f"Text1: '{text1}', Text2: '{text2}'")
        print(f"  LCS (substring): '{substring}'\n")
    
    print()

# ============================================================
# EXERCISE 4: Wildcard Matching
# ============================================================

def wildcard_matching():
    """
    Match string with wildcards (* and ?).
    
    TODO: * matches any sequence, ? matches single char
    """
    print("--- Exercise 4: Wildcard Matching ---")
    
    def is_match(s, p):
        """Check if s matches pattern p"""
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        
        # Handle patterns like *, **, *** at start
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[0][j] = dp[0][j-1]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j-1] == '*':
                    # * matches empty or any sequence
                    dp[i][j] = dp[i][j-1] or dp[i-1][j]
                elif p[j-1] == '?' or s[i-1] == p[j-1]:
                    # ? matches single char or exact match
                    dp[i][j] = dp[i-1][j-1]
        
        return dp[m][n]
    
    test_cases = [
        ("aa", "a"),
        ("aa", "*"),
        ("cb", "?a"),
        ("adceb", "*a*b"),
        ("acdcb", "a*c?b")
    ]
    
    for s, p in test_cases:
        match = is_match(s, p)
        print(f"String: '{s}', Pattern: '{p}'")
        print(f"  Match: {match}\n")
    
    print()

# ============================================================
# EXERCISE 5: Regular Expression Matching
# ============================================================

def regex_matching():
    """
    Match string with regex (. and *).
    
    TODO: . matches any char, * matches 0+ of previous
    """
    print("--- Exercise 5: Regular Expression Matching ---")
    
    def is_match_regex(s, p):
        """Check if s matches regex p"""
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        
        # Handle patterns like a*, a*b*, etc.
        for j in range(2, n + 1):
            if p[j-1] == '*':
                dp[0][j] = dp[0][j-2]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j-1] == '*':
                    # * matches 0 of previous
                    dp[i][j] = dp[i][j-2]
                    # * matches 1+ of previous
                    if p[j-2] == '.' or p[j-2] == s[i-1]:
                        dp[i][j] = dp[i][j] or dp[i-1][j]
                elif p[j-1] == '.' or p[j-1] == s[i-1]:
                    dp[i][j] = dp[i-1][j-1]
        
        return dp[m][n]
    
    test_cases = [
        ("aa", "a"),
        ("aa", "a*"),
        ("ab", ".*"),
        ("aab", "c*a*b"),
        ("mississippi", "mis*is*p*.")
    ]
    
    for s, p in test_cases:
        match = is_match_regex(s, p)
        print(f"String: '{s}', Pattern: '{p}'")
        print(f"  Match: {match}\n")
    
    print()

# ============================================================
# EXERCISE 6: Distinct Subsequences
# ============================================================

def distinct_subsequences():
    """
    Count distinct subsequences of s that equal t.
    
    TODO: Count number of ways
    """
    print("--- Exercise 6: Distinct Subsequences ---")
    
    def num_distinct(s, t):
        """Count distinct subsequences"""
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Empty string has one subsequence: empty
        for i in range(m + 1):
            dp[i][0] = 1
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Don't use s[i-1]
                dp[i][j] = dp[i-1][j]
                
                # Use s[i-1] if it matches t[j-1]
                if s[i-1] == t[j-1]:
                    dp[i][j] += dp[i-1][j-1]
        
        return dp[m][n]
    
    test_cases = [
        ("rabbbit", "rabbit"),
        ("babgbag", "bag"),
        ("aaa", "aa")
    ]
    
    for s, t in test_cases:
        count = num_distinct(s, t)
        print(f"S: '{s}', T: '{t}'")
        print(f"  Distinct subsequences: {count}\n")
    
    print()

# ============================================================
# EXERCISE 7: Interleaving String
# ============================================================

def interleaving_string():
    """
    Check if s3 is interleaving of s1 and s2.
    
    TODO: Maintain order from both strings
    """
    print("--- Exercise 7: Interleaving String ---")
    
    def is_interleave(s1, s2, s3):
        """Check if s3 is interleaving"""
        m, n, l = len(s1), len(s2), len(s3)
        
        if m + n != l:
            return False
        
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        
        # Fill first row (only s2)
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j-1] and s2[j-1] == s3[j-1]
        
        # Fill first column (only s1)
        for i in range(1, m + 1):
            dp[i][0] = dp[i-1][0] and s1[i-1] == s3[i-1]
        
        # Fill rest
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                dp[i][j] = (
                    (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or
                    (dp[i][j-1] and s2[j-1] == s3[i+j-1])
                )
        
        return dp[m][n]
    
    test_cases = [
        ("aabcc", "dbbca", "aadbbcbcac"),
        ("aabcc", "dbbca", "aadbbbaccc"),
        ("", "", "")
    ]
    
    for s1, s2, s3 in test_cases:
        result = is_interleave(s1, s2, s3)
        print(f"S1: '{s1}', S2: '{s2}', S3: '{s3}'")
        print(f"  Is interleaving: {result}\n")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    String DP Problems Complexity:
    
    Common Patterns:
    - 2D DP: dp[i][j] for two strings
    - Time: O(m × n) typically
    - Space: O(m × n) or O(min(m,n)) optimized
    
    Problem Types:
    - Matching: LCS, edit distance, wildcard
    - Palindromes: Longest, count
    - Subsequences: Count, distinct
    - Interleaving: Combine strings
    
    Key Techniques:
    - Build from base cases
    - Consider match/no-match
    - Track positions in both strings
    - Optimize space with rolling arrays
    
    Best Practices:
    - Draw DP table for understanding
    - Handle empty strings
    - Consider space optimization
    - Test edge cases
    
    Common Mistakes:
    - Substring vs subsequence
    - Off-by-one errors
    - Forgetting base cases
    - Not handling empty strings
    
    Security Considerations:
    - Validate string lengths
    - Check for null/empty
    - Limit input sizes
    - Handle Unicode carefully
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 4: String DP Problems")
    print("=" * 60)
    print()
    
    longest_palindrome_substring()
    count_palindromic_substrings()
    longest_common_substring()
    wildcard_matching()
    regex_matching()
    distinct_subsequences()
    interleaving_string()
    
    print("=" * 60)
    print("✅ Day 4 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Most string DP uses 2D table")
    print("2. Consider match/no-match at each position")
    print("3. Palindromes: Expand from center or DP")
    print("4. Pattern matching: Careful with wildcards")


