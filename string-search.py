#!/usr/bin/env python

# Given word W and string S, find the first occurence of W in S. Return a tuple
# (m, c), where m is the start index of the first match and c is the number of
# comparisons you needed. If no match is found, then m should have value None.
# If you compute any other information, which is interesting to inspect, return
# it as the third element of the tuple: (m, c, i)

W = 'aaaaab'
S = 'aaaaaaaaaaab'

#from math import min

# === Straith-forward algorithm ===
# Compare each character in S starting at index m to each character in W, if a
# mismatch is found, increment m by one and compre again until m gets to length
# of S - length of W (where no full match can occur).

# In other words, this algorithm tries to compare each character of S with each
# character of W, until it finds mismatch. If mismatch occurs, it starts over
# beginning with the next character is S and first in W. It leverages no
# knowledge of W.

# The situation is best ilustrated by these W and S:
# W1 = "abcd"
# S1 = "abcXabcd"
# When we get to the 4th character in a mismatch occurs. This algorithm will
# then blindly try to match characters "bcX" in S against "a" in W, effectively 
# wasting time. If we would blincdly skip already matched characters in W, we
# risk the possibility of missing a match as in:
# W3 = "ababX"
# S3 = "abababX"
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

# === Knuth-Morris-Pratt ===
# The worst case with the above is if we have:
# W2 = "aaaab"
# S2 = "aaaaaaaab"
# When we match first 4 'a's a mismatch occurs, then we increment m and match
# again 4 'a's. An inteligent algorithm would know tat there is something
# special on W, which will allow him to skip the 'a' in the beggining of W and
# would continue matching only the last 'b'.

# In KMP algorithm, at every mismatch we try to skip previously matched
# characters in S and in W. To do this we first build a table, let call it
# overlay. This table will tell us, how many characters we can skip in W abd S
# when a mismatch happens at particular position in W.

# For the example of S1 and W1, at first mismatch we can skip all characters
# we already matched in S1 and keep going from the beggining of W1. In the
# example of S2 and W2 we can skip at first mismatch we can skip all matched
# characters in S2 and also W2 and keep going matching only the last character
# in W2.

# To compute the overlay table each character of W with another 'candidate'
# character of W, looking for repeating of the beginning of W inside of W.
# More info http://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
def table_kmp(W):
    wlen = len(W)
    # We create an array [-1, 0, ...] of the length of W
    overlay = [min(i, 0) for i in range(-1, wlen-1)]
    # cnd - Candidate substring index
    cnd = 0
    # pos - Position in table to compute
    pos = 2
    while pos < wlen:
        if W[cnd] == W[pos-1]:
            cnd = cnd + 1
            overlay[pos] = cnd
            pos = pos + 1
        elif cnd > 0:
            cnd = overlay[cnd]
        else:
            cnd = 0
    return overlay

def search_kmp(S, W):
    comps = 0
    overlay = table_kmp(W)
    return (None, comps, overlay)

print "String S: {0} ({1})".format(S, len(S))
print "Word W  : {0} ({1})".format(W, len(W))
print "Straith-forward search: " + str(search(S, W))
print "Knuth-Morris-Prath search: " + str(search_kmp(S, W))
