def largest_twice(nums):
    maxN = secN = idx = 0
    for i in range(len(nums)):
        if (maxN < nums[i]):
            secN = maxN
            maxN = nums[i]
            idx = i
        elif secN < nums[i]:
            secN = nums[i]
    return idx if (maxN >= secN * 2) else - 1