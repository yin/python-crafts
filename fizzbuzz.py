#!/usr/bin/env python

# Create a algorithm, which counts from 1 to a given number max and prints the
# numbers with following exceptions: if the number is divisible by 3 print the
# word 'Fizz' instead, if divisible by 5 print the word 'Buzz'. if divisible by
# both, print both words in the given order.

max = 30

for i in range(1, max + 1):
    out = ''
    if not i % 3:
        out += 'Fizz'
    if not i % 5:
        out += 'Buzz'
    if not out:
        out = str(i)
    print out
        
