def removeDuplicateTwo(nums):
    count = 0
    for i in range(len(nums)):
        if count < 2 or nums[count - 2] != nums[i]:
            nums[count] = nums[i]
            count += 1
    return count

