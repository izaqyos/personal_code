#!/usr/bin/python

"""
usage: du -hsc * | ~/work/scripts/du_sort.py
"""

import sys

UNITS = ["B", "K", "M", "G", "T", "P"]
EXPONENT = dict(zip(UNITS, range(0, len(UNITS))))

class PrefixMultiplierError(Exception):
   pass

def get_prefix_multiplier(unit):
    """ Returns the multiplier corresponding to the given binary prefix. """
    if unit in EXPONENT:
        return 1024 ** EXPONENT[unit]
    else:
        raise PrefixMultiplierError, "Unknown prefix multiplier: %s" % unit

def size_to_bytes(size):
    """ Converts a filesize in a byte multiple to its value in bytes. """
    # some locales use commas as decimal separators
    size = size.replace(",", ".")

    size, unit = size[:-1], size[-1]
    return float(size) * get_prefix_multiplier(unit)

def sort_criterion(line):
    """ Returns the size in bytes or adimensional units of a 'du' output line.
    Defines the sort criterion for 'du' lines in the form 'size filename', where
    size may be adimensional.
    """
    size = line.split()[0]

    if size[-1].isalpha():
        return size_to_bytes(size)
    else: # size given in blocks, don't mess with it
        return float(size)

def sort(input):
    """ Returns a copy of the input list, sorted in ascending order by the first
    column (file size in 'du' output).
    """
    return sorted(input, key=sort_criterion)

def main():
    if len(sys.argv) == 1 or sys.argv[1] == '-':
        input_file = sys.stdin
    else:
        input_file = open(sys.argv[1])

    for line in sort(input_file.readlines()):
        print line.rstrip()

if __name__ == "__main__":
    main()
