#!/usr/bin/env python

# Given an array of capmparable element, such as numbers, of length N, return
# another array of the same elements, such that the elements appear in order
# given by some comparison function.
# In other words, if we choose two elements from returned array L and R, where
# index of R is higher that index of L, the comparison will give always the same
# result (or they are equal).
#
# 1. Use Merge Sort and comparison function L < R.
# 2. Given the array, count all inversions int the array - that is number of
#    pairs of elements in the original array, where the comparison function
#    gives the opposite order.
#
# NOTE: Took 40 minutes brutto to implement

sort_test_set = [
    {
        'input': [5, 4, 1, 8, 7, 2, 6, 3],
        'expected': range(1, 9),
    },
]

count_inversions_test_set = [
    {
        'brief': 'Arbitrary test',
        'input': [1, 3, 5, 2, 4, 6],
        'expected': 3,
    },
    {
        'brief': 'Arbitrary test',
        'input': [5, 4, 1, 8, 7, 2, 6, 3],
        'expected': 15,
    },
    {
        'brief': 'Test for split inversions',
        'input': [1, 3, 2, 4],
        'expected': 1,
    },
    {
        'brief': 'Test ivnersions in the same halves',
        'input': [2, 1, 4, 3],
        'expected': 2,
    },
]

# Solution 1)
def merge_sort(array):
    N = len(array)
    if N < 2:
        return array
    elif N == 2:
        if array[0] < array[1]:
            return array
        else:
            return [array[1], array[0]]
    else:
        left = array[:N/2]
        right = array[N/2:]
        sorted_left = merge_sort(left)
        sorted_right = merge_sort(right)
        return merge(sorted_left, sorted_right)

def merge(left, right):
    Nl = len(left)
    Nr = len(right)
    result = []
    l = 0
    r = 0
    while l < Nl or r < Nr:
        if l == Nl:
            result.append(right[r])
            r += 1
        elif r == Nr:
            result.append(left[l])
            l += 1
        else:
            if left[l] < right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
    return result

# Solution 2)
def count_inversions(array):
    (inversions, sorted) = merge_sort_count_inversions(array)
    return inversions

def merge_sort_count_inversions(array):
    """Returns (count_of_inversions, sorted_array)"""
    N = len(array)
    if N < 2:
        return (0, array)
    elif N == 2:
        if array[0] < array[1]:
            invs = 0
            result = array
        else:
            invs = 1
            result = [array[1], array[0]]
    else:
        left = array[:N/2]
        right = array[N/2:]
        (invs_left, sorted_left) = merge_sort_count_inversions(left)
        (invs_right, sorted_right) = merge_sort_count_inversions(right)
        (invs_split, result) = merge_count_inversions(sorted_left, sorted_right)
        invs = invs_left + invs_right + invs_split
    return (invs, result)

def merge_count_inversions(left, right):
    """Returns (count_of_inversions, sorted_array)"""
    Nl = len(left)
    Nr = len(right)
    result = []
    l = 0
    r = 0
    invs = 0
    while l < Nl or r < Nr:
        if l == Nl:
            result.append(right[r])
            r += 1
        elif r == Nr:
            result.append(left[l])
            l += 1
        else:
            if left[l] < right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
                invs += Nl - l
    return (invs, result)

if __name__ == '__main__':
    i = 0
    for test in sort_test_set:
        i += 1
        print "=== Merge sort test %d ===" % (i)
        print "Input:    {0}".format(test['input'])
        print "Expected: {0}".format(test['expected'])
        result = merge_sort(test['input'])
        print "Actual:   {0}".format(result)
        print ""

    for test in count_inversions_test_set:
        i += 1
        print "=== Count inversions test %d ===" % (i)
        print "Input:    {0}".format(test['input'])
        print "Expected: {0}".format(test['expected'])
        result = count_inversions(test['input'])
        print "Actual:   {0}".format(result)
        print ""
