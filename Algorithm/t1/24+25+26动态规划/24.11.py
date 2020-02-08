def numTrees(n):
    if n <= 2:
        return n
    sol = [0] * (n + 1)
    sol[0] = sol[1] = 1
    for i in range(2, n + 1):
        for left in range(0, i):
            sol[i] += sol[left] * sol[i - 1 - left]
    return sol[n]

def maxProduct(nums):
    if len(nums) == 0:
        return 0
    maximum = minimum = result = nums[0]

    for i in range(1, len(nums)):
        maximum, minimum = max(maximum * nums[i], minimum * nums[i], nums[i]), min(maximum * nums[i], minimum * nums[i], nums[i])
        result = max(result, maximum)
    return result