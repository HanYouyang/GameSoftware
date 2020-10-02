import time
def shell_sort(nums):
    start = time.time()

    gap = len(nums)
    length = len(nums)

    while gap > 0:
        for i in range(gap, length):
            for j in range(i, gap - 1, - gap):
                if (nums[j - gap] > nums[j]):
                    nums[j], nums[j - gap] = nums[j - gap], nums[j]
        if (gap == 2):
            gap = 1
        else:
            gap = gap // 2
    t = time.time() - start
    return len(nums), t