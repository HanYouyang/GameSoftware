def search_first(alist):
    left, right = 0, 1

    while alist[right] == 0:# 无限流就无限去找
        left = right
        right *= 2

        if right > len(alist):
            right = len(alist) - 1
            break

    return left + search_range(alist[left : right + 1], 1)[0]


from bisect import bisect
def findRadius(houses, heaters):
    heaters.sort()
    ans = 0

    for h in houses:
        hi = bisect(heaters, h)
        left = heaters[hi - 1] if hi - 1 >= 0 else float('-inf')
        right = heaters[hi] if hi < len(heaters) else float('inf')
        ans = max(ans, min(h - left, right - h))

    return ans

def sqrt(x):
    if x == 0:
        return 0
    left, right = 1, x
    while left <= right:
        mid = left + (right - left) // 2
        if (mid == x // mid):
            return mid
        if (mid < x // mid):
            left = mid + 1
        else:
            right = mid - 1
    return right