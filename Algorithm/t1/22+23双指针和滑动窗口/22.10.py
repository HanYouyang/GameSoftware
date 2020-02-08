def findCloestElements(alist, k, x):
    left = right = bisect.bisect_left(alist, x)
    while right - left < k:
        if left == 0: return alist[: k]
        if right == len(alist): return alist[-k :]
        if x - alist[left - 1] <= alist[right] - x: left -= 1
        else: right += 1
    return alist[left : right]