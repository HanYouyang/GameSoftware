def minSubarray(alist, target):
    if len(alist) == 0:
        return 0
    i = j = sums = 0
    minium = sys.maxsize

    while j < len(alist):
        sums += alist[j]
        j += 1
        while sums >= target:
            minium = min(minium, j - i)
            sums -= alist[i]
            i += 1
    return 0 if minium == sys.maxsize else minium