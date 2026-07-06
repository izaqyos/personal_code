"""
8. String to Integer (atoi) — v3: overflow-DURING-accumulation
https://leetcode.com/problems/string-to-integer-atoi/

Same spec as v1/v2, but this time solve it AS IF ints were 32-bit signed.
v2 accumulated the full number and clamped at the end — correct in Python only
because ints are unbounded. In C/Java the multiply/add itself overflows the
register BEFORE you ever reach the clamp, so you must detect it one step EARLY.

THE DRILL:
  Before every `ret = ret * 10 + d`, check whether that step is ABOUT to blow
  past the bound, and if so clamp + bail immediately.

  Pre-check algebra (derive it, don't memorize):
        ret * 10 + d > INT_MAX
    <=> ret > (INT_MAX - d) / 10          # move d over, divide by 10
    use FLOOR division so the boundary digit lands on the right side.

  Handle both directions. Two clean ways to structure it:
    (a) accumulate magnitude as a positive number, compare against a ceiling
        that depends on sign (INT_MAX vs abs(INT_MIN) = INT_MAX + 1), or
    (b) accumulate the signed value and check against INT_MAX / INT_MIN
        separately on each branch.
  Pick one and say out loud why the asymmetry (|INT_MIN| = INT_MAX + 1) is safe.

  On detected overflow: return INT_MAX (positive) or INT_MIN (negative) NOW —
  you do not need to keep reading digits, the answer can't change.

Spec reminders (unchanged from v2):
  1. Skip leading whitespace — only ' ' counts (not \\t, \\n).
  2. Optional single sign '+'/'-' (default '+').
  3. Read consecutive digits, stop at first non-digit / end.
  4. No digits read -> 0.

INTERVIEW SOUNDBITE to be able to say:
  "In Python this clamp-at-end works because ints are arbitrary precision;
   with a fixed-width register I'd check `ret > (INT_MAX - d)//10` before the
   multiply, because the overflow corrupts the value before any end-clamp runs."
"""

INT_MIN = -2 ** 31          # -2147483648
INT_MAX = 2 ** 31 - 1       #  2147483647


def my_atoi(s: str) -> int:
    # TODO: implement with overflow detection DURING digit accumulation.
    # Do NOT accumulate the whole number and clamp at the end — that's v2.
    # Guard `ret > (INT_MAX - d) // 10` (adjust for sign) before ret = ret*10 + d.
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

    limit =  INT_MAX + 1  if sign == -1  else INT_MAX      # |INT_MIN| = INT_MAX + 1
    if c == '+' or c == '-':   # sign
        if c == '-':
            sign = -1
        i += 1
    #print(f"skipped leading sign, position is {i}")
    while i < len(s) and s[i].isdigit():  
        c = s[i]
        d = int(c)
        if  ret > (limit - d)  // 10 :
            return INT_MIN if sign == -1 else INT_MAX
        ret = ret * 10 + d

        i += 1

    ret *= sign

    return ret


if __name__ == "__main__":
    cases = [
        # --- basic / spec ---
        ("42", 42),
        ("   -42", -42),
        ("4193 with words", 4193),
        ("words and 987", 0),
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
        ("   +0 123", 0),

        # --- exact bounds (must NOT trip the overflow guard) ---
        ("2147483647", 2147483647),      # exact INT_MAX
        ("-2147483648", -2147483648),    # exact INT_MIN (the asymmetric one)

        # --- one PAST the bound (guard must fire on the LAST digit) ---
        ("2147483648", 2147483647),      # INT_MAX + 1 -> clamp
        ("-2147483649", -2147483648),    # INT_MIN - 1 -> clamp

        # --- overflow mid-accumulation, well before end of digits ---
        ("21474836460", 2147483647),     # ~10x, guard fires early
        ("-91283472332", -2147483648),
        ("9223372036854775808", 2147483647),   # beyond 64-bit
        ("99999999999999999999999999", 2147483647),  # far past, must not hang/err
        ("-99999999999999999999999999", -2147483648),

        # --- overflow then junk: bail early, ignore the tail ---
        ("2147483648 apples", 2147483647),
        ("214748364700000 with words", 2147483647),
    ]
    passed = 0
    for inp, exp in cases:
        print(f"Testing: {inp!r}")
        got = my_atoi(inp)
        status = "PASS" if got == exp else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"{status} | atoi({inp!r}) = {got}  (expected {exp})")
    print(f"\n{passed}/{len(cases)} passed")
