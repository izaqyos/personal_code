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


def encode(strs: list[str]) -> str:
    pass


def decode(s: str) -> list[str]:
    pass


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
