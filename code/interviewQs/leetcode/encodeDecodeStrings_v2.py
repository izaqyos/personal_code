"""
271. Encode and Decode Strings  — VARIANT 2: length-prefix + '#' separator

https://leetcode.com/problems/encode-and-decode-strings/

Design encode/decode for a list of strings sent over the network. May NOT use
eval / serialize / built-in encode-decode libs. Strings may contain ANY of the
256 ASCII chars (including '#', digits, backslashes, whatever).

Constraints:
- 0 <= strs.length < 200
- 0 <= strs[i].length < 200
- strs[i] contains any possible characters out of 256 valid ASCII characters.

Example: ["lint","code","love","you"] -> "4#lint4#code4#love3#you" -> back.

------------------------------------------------------------------------------
This variant vs. the v1 fixed-width header:
- v1 (encodeDecodeStrings.py): one count header + all lengths zero-padded to 3
  digits up front, then payload. Capped at 3-digit lengths.
- v2 (here): per-string `len#str`, no global count, no padding. Handles
  arbitrarily long strings.

Strategy:
  encode(strs) -> str
    For each s: emit  str(len(s)) + "#" + s   and concatenate.
    Layout:  L0 # s0  L1 # s1  L2 # s2 ...   (Ln = decimal length, variable width)

  decode(s) -> list[str]
    Walk with a running position `i`:
      1. Read DIGITS starting at i until you hit the '#'  -> that's the length.
      2. The content starts one char past the '#'. JUMP exactly `length` chars.
      3. Append that slice; advance i to the end of it; repeat until i == len(s).

  KEY: you find the '#' by scanning *digits* (the length field is pure digits,
  so the first non-digit is unambiguously the separator). You reach content by
  JUMPING `length` chars — you never scan content for a '#'. So content can hold
  '#' freely. NO escaping needed. (Escaping here = re-blending the two schemes.)

  Edge cases the tests below probe: empty list (-> ""), empty strings (len 0),
  '#' inside content, content that looks like "4#hello" (a fake length-prefix).
------------------------------------------------------------------------------
"""


def encode(strs: list[str]) -> str:
    parts = [ f"{len(s)}#{s}" for s in strs  ]
    return "".join(parts)


def decode(s: str) -> list[str]:
  prev,pos = 0,0
  strs = []
  while pos < len(s):
    if s[pos] == '#':
      str_len = int(s[prev:pos])
      strs.append(s[pos+1: pos+1+str_len])
      pos = pos +1 + str_len
      prev = pos
    pos+=1

  return strs


if __name__ == "__main__":
    tests = [
        ["lint", "code", "love", "you"],
        ["we", "say", ":", "yes"],
        [],                                       # empty list
        [""],                                     # one empty string
        ["", "", ""],                             # multiple empty strings
        ["hello"],                                # single string
        ["a", "b", "c"],                          # single chars
        ["with space", "tab\there", "newline\n"], # whitespace
        ["#", "##", "###"],                       # contains the separator char
        ["4#hello", "3#hi"],                      # looks like a length-prefix
        ["", "nonempty", ""],                     # empty among non-empty
        ["1234567890" * 25],                      # 250 chars — multi-digit length, > v1's 3-digit cap
    ]
    passed = 0
    for i, original in enumerate(tests):
        encoded = encode(original)
        decoded = decode(encoded)
        status = "PASS" if decoded == original else "FAIL"
        if status == "PASS":
            passed += 1
        print(f"Test {i+1}: {status} | original={original}")
        if status == "FAIL":
            print(f"         encoded={encoded!r}")
            print(f"         decoded={decoded}")
    print(f"\n{passed}/{len(tests)} passed")
