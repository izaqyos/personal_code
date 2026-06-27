"""
271. Encode and Decode Strings
https://leetcode.com/problems/encode-and-decode-strings/

Design an algorithm to encode a list of strings to a string. The encoded string
is then sent over the network and is decoded back to the original list of strings.

Implement the encode and decode methods.

You are not allowed to solve the problem using any serialize methods (such as
eval) or built-in encode/decode library functions.

Notes:
- The string may contain any possible characters out of 256 valid ASCII characters.
  Your algorithm should be generalized enough to work on any possible characters.
- Do not rely on any library method such as eval or serialize.

Constraints:
- 0 <= strs.length < 200
- 0 <= strs[i].length < 200
- strs[i] contains any possible characters out of 256 valid ASCII characters.

Example 1: ["lint","code","love","you"] -> "lint:;code:;love:;you" -> ["lint","code","love","you"]
Example 2: ["we", "say", ":", "yes"] -> "we:;say:;:;yes" -> ["we","say",":","yes"]

Key challenge: the input strings can contain ANY characters — including whatever
delimiter you pick. Think about how to make encoding unambiguous.
"""

"""
  # --- Strategy: fixed-width 3-digit length-prefix header ---
  #
  # encode(strs) -> str
  #   1. Header, all numbers zero-padded to exactly 3 digits (000-199):
  #        [count] [len(strs[0])] [len(strs[1])] ... [len(strs[n-1])]
  #   2. Payload: all strings concatenated, NO delimiter.
  #   Layout:  CCC L0L0L0 L1L1L1 ... <s0><s1>...
  #
  # decode(s) -> list[str]
  #   1. Read count   = int(s[0:3])
  #   2. Read the `count` lengths from the header (3 chars each),
  #      starting at offset 3.
  #   3. Walk the payload with a running offset:
  #        for each length L: take s[off:off+L], then off += L
  #
  # Why no delimiter is needed: lengths are known up front, so we read
  # each string by count instead of scanning for a separator — works for
  # ANY characters (including '#', ':', digits that look like a header).
  #
  # Invariant: every number is EXACTLY 3 chars. Padding is load-bearing.
"""

def encode(strs: list[str]) -> str:
    parts = [f"{len(strs):03d}", *(f"{len(s):03d}" for s in strs), *strs ]
    return "".join(parts)
   



def decode(s: str) -> list[str]:
    strs_len=int(s[:3])
    strs = []
    next_str_pos = (strs_len+1)*3
    for i in range(strs_len):
        len_str = int(s[(i+1)*3: (i+2)*3])
        t_str = s[next_str_pos: next_str_pos + len_str]
        next_str_pos += len_str 
        strs.append(t_str)
    return strs



if __name__ == "__main__":
    tests = [
        ["lint", "code", "love", "you"],
        ["we", "say", ":", "yes"],
        [],                                      # empty list
        [""],                                    # one empty string
        ["", "", ""],                            # multiple empty strings
        ["hello"],                               # single string
        ["a", "b", "c"],                         # single chars
        ["with space", "tab\there", "newline\n"], # whitespace
        ["#", "##", "###"],                      # tricky: contains common delimiter char
        ["4#hello", "3#hi"],                     # tricky: looks like length-prefix encoding
        ["", "nonempty", ""],                    # empty among non-empty
    ]
    for i, original in enumerate(tests):
        encoded = encode(original)
        decoded = decode(encoded)
        status = "PASS" if decoded == original else "FAIL"
        print(f"Test {i+1}: {status} | original={original}")
        if status == "FAIL":
            print(f"         encoded={encoded!r}")
            print(f"         decoded={decoded}")
