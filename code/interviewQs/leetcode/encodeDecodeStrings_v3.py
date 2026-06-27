r"""
271. Encode and Decode Strings  — VARIANT 3: escaping, NO length prefix

https://leetcode.com/problems/encode-and-decode-strings/

Design encode/decode for a list of strings. May NOT use eval / serialize /
built-in encode-decode libs. Strings may contain ANY of the 256 ASCII chars —
including '#' and '\\' (the delimiter and the escape char themselves).

Constraints:
- 0 <= strs.length < 200
- 0 <= strs[i].length < 200
- strs[i] contains any possible characters out of 256 valid ASCII characters.

------------------------------------------------------------------------------
This variant vs. v1 / v2:
- v1 (fixed-width header) and v2 (len#str): both carry LENGTHS, so decode JUMPS
  by length and never scans content. Content needs no escaping.
- v3 (here): NO lengths at all. Strings are separated by a delimiter and decode
  SCANS for it. Because we scan, any delimiter char inside content MUST be
  escaped or it'll be misread as a boundary. This is the approach LC 271 warns
  is error-prone — which is exactly why it's worth drilling.

Scheme (mine — Claude gave food for thought on the two design decisions below,
and I nailed the rest):
  - Delimiter = bare '#', used as a TERMINATOR after every string.
  - Escape rule on content, applied IN THIS ORDER:
        1. '\'  -> '\\'   (escape the escape char FIRST)
        2. '#'  -> '\#'   (then escape the delimiter)
    Order is load-bearing: escaping '#' first would re-double the '\' it
    introduces ('#' -> '\#' -> '\\#'), corrupting the output.

  decode disambiguation — scan left to right:
    - '\'        -> next char is LITERAL content: emit it, consume BOTH chars.
    - bare '#'   -> current string ends here (terminator).
  Unambiguous because every content '\' and '#' is escaped, so the only bare '#'
  left in the stream is a real terminator, and every '\' is always followed by
  exactly one literal char.

Design decisions (resolved):
  1. TERMINATOR, not separator. Terminator keeps []  / [""]  / ["",""] distinct
     ("" / "#" / "##"); a separator collides the first two.
  2. A content string can BE '\#' or worse — the escape step neutralizes it
     before it ever reaches decode (see the brutal tests below).
------------------------------------------------------------------------------
"""


def encode(strs: list[str]) -> str:
    # my next loop does the same, but I like explicit corner-case handling
    ret_str = ""
    if not strs:
        return ret_str

    enc_word_parts = []
    for word in strs:
        for c in word:
            if c == "\\" or c == "#":
                enc_word_parts.append("\\")
                enc_word_parts.append(c)
            else:
                enc_word_parts.append(c)
        enc_word_parts.append("#")

    ret_str += "".join(enc_word_parts)
    return ret_str


def decode(s: str) -> list[str]:
    ret_strs = []
    if not s:
        return ret_strs

    i = 0
    cur_word = []
    while i < len(s):
        c = s[i]
        if c == "#":
            ret_strs.append("".join(cur_word))
            cur_word = []
        elif c == "\\":
            d = s[i + 1]  # last char is always '#', so i+1 is in bounds
            cur_word.append(d)
            i += 1
        else:
            cur_word.append(c)
        i += 1

    return ret_strs
        



if __name__ == "__main__":
    # NOTE on Python literals: "\\" is ONE backslash; "\\#" is backslash+'#'
    # (the literal delimiter token); "\\\\" is TWO backslashes.
    tests = [
        ["lint", "code", "love", "you"],
        [],                                       # empty list   ── must stay
        [""],                                     # one empty    ── distinct from
        ["", "", ""],                             # three empties ── each other
        ["hello"],
        ["#", "##", "###"],                       # bare '#' in content — stays bare, NOT escaped
        ["\\"],                                   # a single backslash — must be escaped
        ["\\\\"],                                 # two backslashes
        ["a\\"],                                  # trailing backslash (escape char at the very end)
        ["\\#"],                                  # content IS the delimiter token — hardest case
        ["\\#hello", "world"],                    # delimiter token embedded in content
        ["with space", "tab\there", "newline\n"], # whitespace
        ["", "nonempty", ""],                     # empty among non-empty
    ]
    passed = 0
    for i, original in enumerate(tests):
       #print(f"Test {i+1} / {len(tests)}")
       encoded = encode(original)
       #print(f"encoded = {encoded}")
       decoded = decode(encoded)
       status = "PASS" if decoded == original else "FAIL"
       if status == "PASS":
           passed += 1
       print(f"Test {i+1}: {status} | original={original}")
       if status == "FAIL":
           print(f"         encoded={encoded!r}")
           print(f"         decoded={decoded}")
    print(f"\n{passed}/{len(tests)} passed")
