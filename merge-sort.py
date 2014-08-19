#!/usr/bin/env python

# NOTE: Took 40 minutes brutto to implement

sort_test_set = [
    {
        'input': [5, 4, 1, 8, 7, 2, 6, 3],
        'expected': range(1, 9),
    }
]

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
