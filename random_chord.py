#!/usr/bin/env python3

"""
show a random chord
(only major and minor)
"""

from random import choice 
from time import sleep

chords = 'C C# D D# E F F# G G# A Bb B'.split()
variations = ['', 'm']

while True:
    print(choice(chords) + choice(variations))
    sleep(1.7)


