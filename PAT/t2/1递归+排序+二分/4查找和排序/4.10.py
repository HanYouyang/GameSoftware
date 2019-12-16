def _merge(a: list, b: list):#  -> list
    c = []
    while len(a) > 0 and len(b) > 0:
        if a[0] < b[0]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    # 直接加上即可不用挨个走了
    if len(a) == 0:
        c += b
    else:
        c += a
    return c

# 真的就是二分
def _merge_sorted(nums: list):
    if len(nums) <= 1:
        return nums
    
    m = len(nums) // 2
    a = _merge_sorted(nums[ : m])
    b = _merge_sorted(nums[m : ])
    return _merge(a, b)

import time
def merge_sorted(nums: list, reverse = False):
    start = time.time()
    
    nums = _merge_sorted(nums)
    if reverse:
        nums = nums[ : : - 1]
    
    t = time.time() - start
    return len(nums), t