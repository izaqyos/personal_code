#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculates the size of a string (read from standard input)
in bytes when encoded as UTF-8.
This is the encoding used by HTTP body and headers so it's important to know the size of the string.
"""

import sys

def calculate_utf8_size(input_str):
    """
    Encodes a string using UTF-8 and returns its size in bytes.

    Args:
        input_str (str): The string to measure.

    Returns:
        int: The size of the string in bytes when UTF-8 encoded.
    """
    try:
        # Encode the string into bytes using UTF-8
        utf8_bytes = input_str.encode('utf-8')
        # Return the length of the resulting byte sequence
        return len(utf8_bytes)
    except Exception as e:
        # Handle potential encoding errors
        print(f"Error encoding string: {e}", file=sys.stderr)
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    """
    Main execution block: Reads all standard input until EOF
    and prints the UTF-8 byte size.
    """
    try:
        # Inform the user how to provide input, printing to stderr
        # so it doesn't interfere with piped output.
        if sys.stdin.isatty(): # Check if running interactively in a terminal
             print("Reading from standard input. Paste your text now.", file=sys.stderr)
             print("Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) when done.", file=sys.stderr)

        # Read ALL data from standard input until EOF is signaled
        user_input = sys.stdin.read()

        # Check if any input was actually received
        if not user_input:
             # Only print message if interactive, otherwise might be valid empty pipe
             if sys.stdin.isatty():
                  print("\nNo input received.", file=sys.stderr)
             sys.exit(0) # Exit cleanly if no input

        # Calculate the size
        byte_size = calculate_utf8_size(user_input)

        # Print the final result to standard output
        # (stdout allows piping the result to other commands if needed)
        print(f"{byte_size}")

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)