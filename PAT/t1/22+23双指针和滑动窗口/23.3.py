def removeElement(nums, val):
    i = 0
    for j in range(len(nums)):
        if nums[j] != val:
            nums[i] = nums[j]
            i += 1
    return i
def removeElement2(nums, val):
    start, end = 0, len(nums) - 1
    while start <= end:
        if nums[start] == val:
            nums[start], end = nums[end], end - 1
        else:
            start += 1
    return start
