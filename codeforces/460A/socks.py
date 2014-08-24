#!/usr/bin/env python

# From:
# http://codeforces.com/problemset/problem/460/A

# This solution is WRONG
def vasya_socks_bruteforce(n, m):
    new_socks = int(n / m)
    print new_socks
    if new_socks != 0:
        return n + vasya_socks_bruteforce(new_socks, m)
    else:
        return n

# This solution was adapted from another solution, time O(N/M)
def vasya_socks_leaked(n, m):
    result = n
    while n >= m:
        result += n / m
        n = n / m + n % m
    return result

from math import ceil, floor

# This solution tries to compute the number of days in time O(1). There are two
# functions, the function of socks left each day:
# f1: y = -x + n
# and the function of new socks bought:
# f2: y = 1/m * x
# The total number of days is then given by the sumation of f1 and f2:
# f: y = f1(x) + f2(x) = (1.0 - 1/m)*x + n
# It is the solution to x of:
# 1 > f(x) >= 0  =>  0 = (1.0 - 1/m)*x + n  (plus a small fraction)
# The solution comes out as x = n / (1/m - 1)
def vasya_socks(n, m):
    return -int((n) / (1.0/m - 1) + (1.0/m))

if __name__ == '__main__':
    my_input = map(int, raw_input().split())
    print "WRONG recursive bruteforce: ", vasya_socks_bruteforce(my_input[0], my_input[1])
    print "Solution from someone:      ", vasya_socks_leaked(my_input[0], my_input[1])
    print "My solution O(1):           ", vasya_socks(my_input[0], my_input[1])
