def getCumulateSum(n):
    return (n * (n + 1)) // 2
def minDaysToEmpty(c, ll):
    if c <= ll:
        return c
    l, h = 0, 1e4

    while l < h:
        mid = int((l + h) // 2)

        if getCumulateSum(mid) >= (c - ll):
            h = mid
        else:
            l = mid + 1
        
    return (l + ll)

