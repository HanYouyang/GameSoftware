def _quick_sorted(nums:list):
    if len(nums) <= 1:
        return nums
    
    pivot = nums[0]
    left_nums = _quick_sorted([x for x in nums[1 : ] if x < pivot])
    right_nums = _quick_sorted([x for x in nums[1 : ] if x >= pivot])
    return left_nums + [pivot] + right_nums

import time
def quick_sorted(nums: list, reverse = False):
    start = time.time()
    
    nums = _quick_sorted(nums)
    if reverse:
        nums = nums[ : : - 1]
    
    t = time.time() - start
    return len(nums), t