def findLengthOfLCIS(nums):
    result, count = 0, 0
    for i in range(len(nums)):
        if i == 0 or nums[i - 1] < nums[i]:
            count += 1
            result = max(result, count)
        else:
            count = 1
    return result

