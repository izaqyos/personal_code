import unittest
import sys
import os

from utf8_sizer import calculate_utf8_size

class TestUtf8Sizer(unittest.TestCase):

    def test_empty_string(self):
        """Test with an empty string."""
        self.assertEqual(calculate_utf8_size(""), 0)

    def test_basic_ascii(self):
        """Test with standard ASCII characters (1 byte each)."""
        self.assertEqual(calculate_utf8_size("hello"), 5)
        self.assertEqual(calculate_utf8_size("12345"), 5)
        self.assertEqual(calculate_utf8_size("!@#$%"), 5)

    def test_latin1_chars(self):
        """Test with characters typically using 2 bytes in UTF-8."""
        self.assertEqual(calculate_utf8_size("résumé"), 8) # é is 2 bytes
        self.assertEqual(calculate_utf8_size("你好"), 6) # 你 and 好 are 3 bytes each in UTF-8
        self.assertEqual(calculate_utf8_size("€"), 3)    # Euro sign is 3 bytes

    def test_multi_byte_chars(self):
        """Test with characters requiring more bytes."""
        self.assertEqual(calculate_utf8_size("你好世界"), 12) # 4 chars * 3 bytes/char
        self.assertEqual(calculate_utf8_size("😊"), 4)     # Emoji is 4 bytes

    def test_mixed_chars(self):
        """Test with a mix of ASCII and multi-byte characters."""
        self.assertEqual(calculate_utf8_size("Hello 你好 😊"), 17) # 5 (Hello) + 1 (space) + 6 (你好) + 1 (space) + 4 (😊)

    def test_non_breaking_spaces(self):
        """Test with non-breaking spaces (U+00A0, 2 bytes in UTF-8)."""
        # "a b c" with NBSP between a and b
        test_string = "a\u00A0b c"
        # Expected size: 1 (a) + 2 (NBSP) + 1 (b) + 1 (space) + 1 (c) = 6 bytes
        self.assertEqual(calculate_utf8_size(test_string), 6)
        # Test with multiple NBSPs
        test_string_multi = "\u00A0\u00A0Hello\u00A0"
        # Expected size: 2 (NBSP) + 2 (NBSP) + 5 (Hello) + 2 (NBSP) = 11 bytes
        self.assertEqual(calculate_utf8_size(test_string_multi), 11)

    def test_longer_text(self):
        """Test with a longer piece of text."""
        text = "This is a longer text with some special characters like é, ü, and ç. Also includes € and maybe 😊."
        # Calculate expected size manually or using a known good reference:
        # This: 4
        #  is : 3
        #  a  : 2
        # longer: 7
        #  text: 5
        #  with: 5
        #  some: 5
        #  special: 8
        #  characters: 11
        #  like: 5
        #  é,: 3 (é=2, ,=1)
        #  ü,: 3 (ü=2, ,=1)
        #  and: 4
        #  ç.: 3 (ç=2, .=1)
        #  Also: 5
        #  includes: 9
        #  €: 4 (space=1, €=3)
        #  and: 4
        #  maybe: 6
        #  😊.: 5 (space=1, 😊=4)  <- Corrected: Emoji is 4 bytes, . is 1 byte
        # Expected: 4+3+2+7+5+5+5+8+11+5+3+3+4+3+5+9+4+4+6+5 = 106 (Corrected based on actual encoding)
        expected_size = len(text.encode('utf-8')) # Use Python's encoding as reference
        self.assertEqual(calculate_utf8_size(text), expected_size)

if __name__ == '__main__':
    unittest.main() 