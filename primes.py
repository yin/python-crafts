#!/usr/bin/env python

# Find all primes up to a maximum number N, say the default is 150. Bonus points
# will be given to you if you find also the non-primes in that range.

import sys
import math

N = 150
if len(sys.argv) > 1:
    try:
        N = int(sys.argv[1])
    except ValueError:
        pass

# Taken from http://www.secnetix.de/olli/Python/list_comprehensions.hawk

# We need the root to get all non-primes, we will generate all the
# multiples of each number from 4 (smallest non-prime) to root
# It is not square root.
root = int(math.ceil(math.sqrt(N)))

# Now generate all the possible non-primes. They will be repeated, e.g.
# for N=8 -> [4, 6, 8, 6]
noprimes = [j for i in range(2, root+1) for j in range(i*2, N+1, i)]

# Now just find what's missing in non-primes and that are our primes
primes=[x for x in range(2, N+1) if x not in noprimes]

print "Non-primes: " + str(noprimes)
print "Primes    : " + str(primes)
