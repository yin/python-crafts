#!/usr/bin/env python

# 1. Given word W and string S, find the first occurence of W in S. Return a
# tuple (m, c), where m is the start index of the first match and c is the
# number of comparisons you needed. If no match is found, then m should have
# value None. If you compute any other information, which is interesting to
# inspect, return it as the third element of the tuple: (m, c, i)
# 2. Implement Knuth-Morris-Pratt aka KMP algorithm. Compute the kmp_table in a
# separate function.

search_test_sets = [
    {
        'word': 'abcd',
        'string': 'abcXabcd',
        'results': [4],
    },
    {
        'word': 'aaaab',
        'string': 'aaaaaaaab',
        'results': [4],
    },
    {
        'word': 'ababX',
        'string': 'abababX',
        'results': [2],
    },
]
kmp_table_test_sets = [
    {
        # This one server for KMP
        'pattern': 'abcdababcdab',
        'results': [-1, 0, 0, 0, 0, 1, 2, 1, 2, 3, 4, 5],
    },
    {
        # This one server for KMP
        'pattern': 'ababcdababcd',
        'results': [-1, 0, 0, 1, 2, 0, 0, 1, 2, 3, 4, 5],
    },
]

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
# kmp_table. This table will tell us, how many characters we can skip in W and S
# when a mismatch happens at particular position in W.

# For the example of S1 and W1, at first mismatch we can skip all characters
# we already matched in S1 and keep going from the beggining of W1. In the
# example of S2 and W2 we can skip at first mismatch we can skip all matched
# characters in S2 and also W2 and keep going matching only the last character
# in W2.

# To compute the kmp_table compare each character of W with another
# 'candidate' character of W, looking for repeating of the beginning of W
# inside of W. Put the index of candidate in table at each match, at mismatch
# reset candidate index to 0.
# More info bellow, or at
# http://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
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
            overlay[pos] = 0
            pos = pos + 1
    return overlay

# While searching we'll use the KMP table to tell us how to change values
# of m and i. In the algorithm bellow, we are first interested in a match. If we
# are matching successfully, we keep attention to i, which tells us, when we
# have reached the end end word W. If an mismatch occurs somewhere in the middle
# of W we use the table to tell us how much to increase m and what to value set
# i. At the beginning of W, we haven matched even the first character, so we
# increment m and keep i to 0. An intuition is given in KMP table test bellow.
def search_kmp(S, W):
    comps = 0
    table = table_kmp(W)
    lens = len(S)
    lenw = len(W)
    m = 0
    i = 0
    while m+i < lens:
        comps = comps + 1
        if S[m+i] == W[i]:
            if i == lenw - 1:
                return (m, comps, table)
            else:
                i = i + 1
        else:
            if table[i] > -1:
                i = table[i]
                m = m + i - table[i]
            else:
                i = 0
                m = m + 1
    return (None, comps, table)

if __name__ == '__main__':
    i = 0
    # here we test the search functions
    for test in search_test_sets:
        i = i + 1
        W = test['word']
        S = test['string']
        results = test['results']
        
        print "=== String-search test %d ===" % (i)
        print "String S: {0} ({1})".format(S, len(S))
        print "Word W  : {0} ({1})".format(W, len(W))
        print "Expected results: {0}".format(results)
        (index, comps) = search(S, W)
        print "Straith-forward search: {0}, comparisons: {1}".format(index, comps)
        (index, comps, kmp) = search_kmp(S, W)
        print "Knuth-Morris-Prath search: {0}, comparisons: {1}".format(index, comps)
        print ''

    # Now let's test the KMP table function, it has more uses than than
    # searching W in S, so it is interesting to see how it looks.
    i = 0
    for test in kmp_table_test_sets:
        i = i + 1
        P = test['pattern']
        results = test['results']
        # Here I format the pattern to fit the KMP tables nicelly
        pretty_P = '[ ' + (', '.join(P)) + ']'

        # After running this, we can see some nice patterns in the results
        print "=== KMP table test %d ===" % (i)
        print "Pattern         : {0} ({1})".format(pretty_P, len(P))
        print "Expected results: {0}".format(results)
        print "KMP table       : " + str(table_kmp(P))
        print ''

        # Here is an excerpt from output of the above:
        # Pattern  : [ a, b, a, b, c, d, a, b, a, b, c, d] (12)
        # KMP table: [-1, 0, 0, 1, 2, 0, 0, 1, 2, 3, 4, 5]

        # Lets rotate the KMP table left:
        # Pattern    : [ a, b, a, b, c, d, a, b, a, b, c,  d] (12)
        # Rotated KMP: [ 0, 0, 1, 2, 0, 0, 1, 2, 3, 4, 5, -1]

        # What we can see an overlap with the pattern now. It was not straigth-
        # -forward at the beginning, but now we can see, what is the table_kmp
        # computing: the number characters matching continously the beginning of
        # the pattern. Every mismatch is denoted as 0 and each match increments
        # the previous number in the table. At the end there is a special value,
        # which marks the end of succesful matching.

        # This is though not what we need to know in a string-matching algorithm
        # in a practical situation. We already know that at every match we are
        # supposed to increase our position in the word and in the string. What
        # we want to know is, what to do, when we mismatch.

        # So the original table tells us actually, how many character would have
        # matched from beginning of the word W. So when we get a mismatch at
        # S[m+i] and W[i], we can safely skip all characters in S, we already
        # tried to match. And the table tells us, where to restart i to not miss
        # any potential matches. Got it now?
