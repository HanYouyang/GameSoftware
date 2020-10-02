def reverse(nums):
    n = len(nums)
    for i in range(len(nums) // 2):
        nums[i], nums[n - 1 - i] = nums[n - 1 - i], nums[i]
    print(nums)

def reverse2(nums):
    i, j = 0, len(nums) - 1
    while i < j:
        nums[i], nums[j] = nums[j], nums[i]
        i += 1
        j -= 1
    print(nums)

