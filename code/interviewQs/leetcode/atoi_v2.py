"""
8. String to Integer (atoi)
https://leetcode.com/problems/string-to-integer-atoi/

Convert a string to a 32-bit signed integer, following these steps IN ORDER:
  1. Skip leading whitespace (only ' ').
  2. Optional single sign: '+' or '-' (default '+').
  3. Read consecutive digits; stop at the first non-digit (or end of string).
     Ignore everything after.
  4. If no digits were read, the result is 0.
  5. Clamp to the 32-bit signed range:
        INT_MIN = -2**31 = -2147483648
        INT_MAX =  2**31 - 1 = 2147483647
     Below INT_MIN -> INT_MIN; above INT_MAX -> INT_MAX.

Edge cases the tests below hammer:
  - leading spaces, then sign, then digits      "   -42"      -> -42
  - trailing junk after digits                  "4193 with words" -> 4193
  - leading non-digit (no conversion)           "words and 987"   -> 0
  - lone sign / double sign                     "+", "-", "+-2"   -> 0
  - leading zeros                               "0032", "  -0012a42"
  - exact bounds                                "2147483647", "-2147483648"
  - overflow / underflow clamp                  "2147483648" -> INT_MAX, "-91283472332" -> INT_MIN
  - non-digit start that looks numeric          ".1", "3.14159" (stops at '.')
  - empty / all-whitespace                      "", "   "

Design decision worth settling before you code:
  Python ints are unbounded, so you CAN accumulate the full number and clamp at
  the very end. In C/Java you'd overflow first, so the "real" interview answer
  detects the overflow DURING accumulation (compare against INT_MAX//10 before
  multiplying). Decide which version you're practicing — the second is the one
  worth being able to write.
"""

INT_MIN = -2 ** 31
INT_MAX = 2 ** 31 - 1


def my_atoi(s: str) -> int:
    ret = 0
    i = 0
    sign = 1
    while i < len(s) and s[i] == ' ':   # skip leading whitespace
        i += 1
    #print(f"skipped leading spaces, position is {i}")
    if i >= len(s):
        return ret 
    if i< len(s):
        c = s[i]
    else:
        return ret 

    if c == '+' or c == '-':   # sign
        if c == '-':
            sign = -1
        i += 1
    #print(f"skipped leading sign, position is {i}")
    while i < len(s) and s[i].isdigit():  
        c = s[i]
        #print(f"processing digit {c}, position is {i}")
        ret = ret * 10 + int(c)
        i += 1

    ret *= sign
    if ret > INT_MAX:
        ret = INT_MAX
    elif ret < INT_MIN:
        ret = INT_MIN

    return ret


if __name__ == "__main__":
    cases = [
        ("42", 42),
        ("   -42", -42),
        ("4193 with words", 4193),
        ("words and 987", 0),
        ("-91283472332", -2147483648),   # underflow -> INT_MIN
        ("2147483648", 2147483647),      # overflow  -> INT_MAX
        ("2147483647", 2147483647),      # exact INT_MAX
        ("-2147483648", -2147483648),    # exact INT_MIN
        ("", 0),
        ("   ", 0),
        ("+", 0),
        ("-", 0),
        ("+-2", 0),
        ("-+2", 0),
        ("0032", 32),
        ("  -0012a42", -12),
        ("+1", 1),
        ("3.14159", 3),
        (".1", 0),
        ("  0000000000012345678", 12345678),
        ("9223372036854775808", 2147483647),  # beyond 64-bit -> clamp
        ("   +0 123", 0),
        ("21474836460", 2147483647),     # 10x INT_MAX-ish overflow
        ("  -2147483649", -2147483648),  # one past INT_MIN -> clamp
    ]
    passed = 0
    for inp, exp in cases:
        print(f"Testing: {inp!r} xx")
        got = my_atoi(inp)
        status = "PASS" if got == exp else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"{status} | atoi({inp!r}) = {got}  (expected {exp})")
    print(f"\n{passed}/{len(cases)} passed")
