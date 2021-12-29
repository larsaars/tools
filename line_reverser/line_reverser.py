#!/usr/bin/python

"""
The first argument shall be a file name.
This file will be read and the lines will be reversed and saved
in a second file named 'filename'-reversed.txt.

example:
    line1
    line2
    line3

will be:
    line3
    line2
    line1
"""

import sys

def reverse_lines(file: str):
    with open(file, 'r') as f:
        reversed = f.readlines()
        reversed.reverse()

        with open(file + '-reversed', 'w') as output_file:
            output_file.write(''.join(reversed))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        reverse_lines(sys.argv[1])
    else:
        print('please specify a file name!')
    
