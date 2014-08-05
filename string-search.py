#!/usr/bin/env python

# Given word W and string S, find the first occurence of W in S. Return a tuple
# (m, c), where m is the start index of the first match and c is the number of
# comparisons you needed. If no match is found, then m should have value None.

W = 'aaaaab'
S = 'aaaaaaaaaaab'

# Straith-forward implementation: compare each character in S starting at
# index m to each character in W, if a mismatch is found, increment m by one
# and compre again until m gets to length of S - length of W (where no full
# match can occur).

def search(S, W):
    comps = 0
    for m in range(0, len(S) - len(W) + 1):
        match = True
        for i in range(0, len(W)):
            comps += 1
            if S[m+i] != W[i]:
                match = False
                break
        if match:
            return (m, comps)
    return (None, comps)

print "String S: {0} ({1})".format(S, len(S))
print "Word W  : {0} ({1})".format(W, len(W))
print "Straith-forward search: " + str(search(S, W))
