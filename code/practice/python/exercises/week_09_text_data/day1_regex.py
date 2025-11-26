"""
Week 9, Day 1: Regular Expressions (re module)

Learning Objectives:
- Master regex patterns
- Learn re module functions
- Practice text matching
- Understand regex groups
- Solve text processing problems

Time: 10-15 minutes
"""

import re
from typing import List, Optional

# ============================================================
# EXERCISE 1: Basic Pattern Matching
# ============================================================

def basic_patterns():
    """
    Learn basic regex patterns.
    
    Regex: Pattern matching for text
    """
    print("--- Exercise 1: Basic Pattern Matching ---")
    
    text = "Contact us at support@example.com or sales@example.org"
    
    # Find email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    print(f"Text: {text}")
    print(f"Emails found: {emails}")
    
    # Check if text contains pattern
    has_email = re.search(email_pattern, text)
    print(f"Contains email: {has_email is not None}")
    
    # Match at beginning
    text2 = "Python is awesome"
    matches_start = re.match(r'Python', text2)
    print(f"\nText: '{text2}'")
    print(f"Starts with 'Python': {matches_start is not None}")
    
    print()

# ============================================================
# EXERCISE 2: Regex Special Characters
# ============================================================

def special_characters():
    """
    Master regex special characters.
    
    TODO: . * + ? ^ $ [] {} () | \\
    """
    print("--- Exercise 2: Special Characters ---")
    
    examples = [
        (r'\d+', "Order 123 costs $45", "Digits"),
        (r'\w+', "hello_world123", "Word characters"),
        (r'\s+', "split   by   spaces", "Whitespace"),
        (r'^Start', "Start of line", "Start anchor"),
        (r'end$', "line end", "End anchor"),
        (r'[aeiou]', "hello", "Character class"),
        (r'[0-9]{3}', "Call 555-1234", "Quantifier"),
        (r'(cat|dog)', "I have a cat", "Alternation"),
    ]
    
    for pattern, text, description in examples:
        matches = re.findall(pattern, text)
        print(f"{description:20} Pattern: {pattern:15} Text: '{text}'")
        print(f"{'':20} Matches: {matches}\n")
    
    print()

# ============================================================
# EXERCISE 3: Groups and Capturing
# ============================================================

def groups_capturing():
    """
    Learn regex groups for extraction.
    
    TODO: Capture parts of matches
    """
    print("--- Exercise 3: Groups and Capturing ---")
    
    # Extract date components
    text = "Date: 2024-03-15"
    pattern = r'(\d{4})-(\d{2})-(\d{2})'
    match = re.search(pattern, text)
    
    if match:
        print(f"Text: {text}")
        print(f"Full match: {match.group(0)}")
        print(f"Year: {match.group(1)}")
        print(f"Month: {match.group(2)}")
        print(f"Day: {match.group(3)}")
        print(f"All groups: {match.groups()}")
    
    # Named groups
    pattern_named = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
    match_named = re.search(pattern_named, text)
    
    if match_named:
        print(f"\nNamed groups:")
        print(f"Year: {match_named.group('year')}")
        print(f"Month: {match_named.group('month')}")
        print(f"Day: {match_named.group('day')}")
        print(f"Dict: {match_named.groupdict()}")
    
    print()

# ============================================================
# EXERCISE 4: Substitution and Replacement
# ============================================================

def substitution():
    """
    Replace text using regex.
    
    TODO: re.sub() for replacements
    """
    print("--- Exercise 4: Substitution and Replacement ---")
    
    # Simple replacement
    text = "The price is $100 and $200"
    new_text = re.sub(r'\$(\d+)', r'€\1', text)
    print(f"Original: {text}")
    print(f"Replaced: {new_text}")
    
    # Using function for replacement
    def double_price(match):
        price = int(match.group(1))
        return f"${price * 2}"
    
    text2 = "Items cost $50, $75, and $100"
    doubled = re.sub(r'\$(\d+)', double_price, text2)
    print(f"\nOriginal: {text2}")
    print(f"Doubled: {doubled}")
    
    # Remove extra whitespace
    text3 = "Too    many     spaces"
    cleaned = re.sub(r'\s+', ' ', text3)
    print(f"\nOriginal: '{text3}'")
    print(f"Cleaned: '{cleaned}'")
    
    print()

# ============================================================
# EXERCISE 5: Splitting Text
# ============================================================

def splitting_text():
    """
    Split text using regex patterns.
    
    TODO: re.split() for complex splitting
    """
    print("--- Exercise 5: Splitting Text ---")
    
    # Split by multiple delimiters
    text = "apple,banana;cherry:date|elderberry"
    parts = re.split(r'[,;:|]', text)
    print(f"Text: {text}")
    print(f"Split: {parts}")
    
    # Split keeping delimiters
    text2 = "Hello! How are you? I'm fine."
    parts2 = re.split(r'([.!?])', text2)
    print(f"\nText: {text2}")
    print(f"Split with delimiters: {parts2}")
    
    # Split by whitespace (multiple)
    text3 = "word1   word2\t\tword3\nword4"
    parts3 = re.split(r'\s+', text3)
    print(f"\nText: '{text3}'")
    print(f"Split: {parts3}")
    
    print()

# ============================================================
# EXERCISE 6: Validation Patterns
# ============================================================

def validation_patterns():
    """
    Common validation patterns.
    
    TODO: Email, phone, URL, etc.
    """
    print("--- Exercise 6: Validation Patterns ---")
    
    validators = {
        'Email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'Phone (US)': r'^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$',
        'URL': r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'IP Address': r'^(\d{1,3}\.){3}\d{1,3}$',
        'Hex Color': r'^#[0-9A-Fa-f]{6}$',
        'Username': r'^[a-zA-Z0-9_]{3,16}$',
    }
    
    test_cases = {
        'Email': ['user@example.com', 'invalid.email', 'test@test.co.uk'],
        'Phone (US)': ['555-123-4567', '(555) 123-4567', '5551234567'],
        'URL': ['https://example.com', 'http://test.org', 'ftp://wrong'],
        'Hex Color': ['#FF5733', '#abc', '#123456'],
    }
    
    for validator_name, pattern in list(validators.items())[:4]:
        print(f"{validator_name}:")
        if validator_name in test_cases:
            for test in test_cases[validator_name]:
                is_valid = bool(re.match(pattern, test))
                status = "✓" if is_valid else "✗"
                print(f"  {status} '{test}'")
        print()
    
    print()

# ============================================================
# EXERCISE 7: Real-World - Log Parser
# ============================================================

def log_parser():
    """
    Parse log files with regex.
    
    TODO: Extract structured data from logs
    """
    print("--- Exercise 7: Log Parser ---")
    
    log_lines = [
        "2024-03-15 10:30:45 ERROR Database connection failed",
        "2024-03-15 10:31:12 INFO User login: john_doe",
        "2024-03-15 10:32:05 WARNING High memory usage: 85%",
        "2024-03-15 10:33:20 ERROR API timeout: /api/users",
    ]
    
    # Pattern for log parsing
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    
    print("Parsed logs:")
    for line in log_lines:
        match = re.match(pattern, line)
        if match:
            date, time, level, message = match.groups()
            print(f"  Date: {date}, Time: {time}")
            print(f"  Level: {level}, Message: {message}\n")
    
    # Count errors
    error_count = sum(1 for line in log_lines if re.search(r'ERROR', line))
    print(f"Total errors: {error_count}")
    
    print()

# ============================================================
# REGEX FLAGS
# ============================================================

def regex_flags():
    """
    Learn regex flags for behavior modification.
    """
    print("--- Regex Flags ---")
    
    text = "Python\npython\nPYTHON"
    
    # Case insensitive
    matches_i = re.findall(r'python', text, re.IGNORECASE)
    print(f"Text: {repr(text)}")
    print(f"Case insensitive matches: {matches_i}")
    
    # Multiline
    text2 = "Start of line\nAnother start\nEnd"
    matches_m = re.findall(r'^[A-Z]', text2, re.MULTILINE)
    print(f"\nMultiline matches: {matches_m}")
    
    # Dotall (. matches newline)
    text3 = "Hello\nWorld"
    match_s = re.search(r'Hello.World', text3, re.DOTALL)
    print(f"\nDotall match: {match_s is not None}")
    
    # Verbose (comments in regex)
    pattern_x = re.compile(r'''
        \d{3}    # Area code
        -        # Separator
        \d{3}    # Exchange
        -        # Separator
        \d{4}    # Number
    ''', re.VERBOSE)
    
    print(f"\nVerbose pattern matches '555-123-4567': {bool(pattern_x.match('555-123-4567'))}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Regex Complexity and Best Practices:
    
    Time Complexity:
    - Simple patterns: O(n) where n is text length
    - Backtracking patterns: Can be exponential!
    - Avoid: (a+)+ or (a*)*
    
    Space Complexity:
    - O(m) for pattern compilation
    - O(k) for matches where k is match count
    
    Best Practices:
    - Compile patterns used repeatedly
    - Use raw strings: r'pattern'
    - Avoid catastrophic backtracking
    - Test patterns thoroughly
    - Use specific patterns over greedy
    
    Common Patterns:
    - \\d: digit [0-9]
    - \\w: word char [a-zA-Z0-9_]
    - \\s: whitespace
    - \\b: word boundary
    - ^: start of string
    - $: end of string
    - .: any character
    - *: 0 or more
    - +: 1 or more
    - ?: 0 or 1
    - {n,m}: n to m times
    
    Security Considerations:
    - Validate input before regex
    - Limit input length
    - Avoid user-supplied patterns
    - Watch for ReDoS attacks
    - Use timeouts for complex patterns
    
    Performance Tips:
    - Compile frequently used patterns
    - Use non-capturing groups: (?:...)
    - Anchor patterns when possible
    - Use character classes efficiently
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9, Day 1: Regular Expressions")
    print("=" * 60)
    print()
    
    basic_patterns()
    special_characters()
    groups_capturing()
    substitution()
    splitting_text()
    validation_patterns()
    log_parser()
    regex_flags()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Regex: Powerful pattern matching")
    print("2. Use raw strings: r'pattern'")
    print("3. Groups capture parts of matches")
    print("4. Compile patterns for reuse")

