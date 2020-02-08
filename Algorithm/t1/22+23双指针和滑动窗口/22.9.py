def sortColors(nums):
    count = [0] * 3
    for num in nums:
        count[num] += 1
    i = 0 
    for j in range(3):
        for _ in range(count[j]):
            nums[i] = j
            i += 1

def sortColors2(nums):
    i, l, r = 0, 0, len(nums) - 1
    while i <= r:
        if nums[i] == 0:
            nums[i], nums[l] = nums[l], nums[i]
            i, l = i + 1, l + 1
        elif nums[i] == 2:
            nums[i], nums[r] = nums[r], nums[i]
            r -= 1
        else:
            i += 1