#!/usr/bin/env python

# Status:
# =======
# The brute force is only good for N < 10e5. It tries all the numbers M from
# 2 to N-1 and count the divisors by iterating divisors from 1 to M/2
#
# A better solution:
# =================
#
# A better way to do this is to
# generate prime numbers p1, p2, .., pk and iterate all possible exponents to
# them to generate the result p1^e1 * p2^e2 * ... * pk * ek. In this case the
# number of divisors is given by formula (e1+1) * (e2+1) * ... * (ek+1).
#
# Problem Description:
# ====================
# From file: tuymaada-2014-day-1-en.docx 
# Kolya and Vasya play a game. A natural number N is randomly selected, and then
# each player must name a natural number not greater than N. The player whose
# number has more divisors wins, and if the two numbers have the same number of
# divisors then the player with the smaller number wins. Note that the divisors
# of any number include both 1 and the number itself. Kolya badly wants to win
# this game and thinks that it would be great to have a program which will input
# and output the required number. Help him to write a program that will find the
# smallest number with the highest number of divisors.
#
# Input format:
# A file named: input.txt
# The input file holds a single natural number N (1 <= N <= 10e16). 
#
# Output format:
# A file named output.txt
# Output the smallest number with the most divisors. The number must not exceed .
#
# Constrains:
# Run time: 1s
# Memory: 64MB
#
# Submit to: http://codeforces.com/gym/100467/submit

def find_max_divisors_product_bruteforce(N):
    result = 1
    divs = 1
    for i in range(2, N):
        divs_i = count_divisors(i)
        if divs_i > divs:
            result = i
            divs = divs_i
    return result

def count_divisors(n):
    divs = 0
    for i in range(1, n/2+1):
        if n % i == 0:
            divs += 1
    return divs

def get_input():
    """if std is true, reads from stdout, else reads file input.txt"""
    if std:
        my_input = raw_input()
    else:
        f = open('input.txt', 'r')
        my_input = f.readline()
        f.close()
    return my_input

def put_output(out):
    """if std is true, prints to stdout, else writes file output.txt"""
    if std:
        print str(out)
    else:
        f = open('output.txt', 'w')
        f.write(out + "\n")
        f.close()

from sys import argv

if __name__ == '__main__':
    std = len(argv) > 1 and argv[1] == '-std'
    my_input = get_input(std)
    N = map(long, my_input.split())[0]
    result = find_max_divisors_product_bruteforce(N)
    put_output(result, std)
