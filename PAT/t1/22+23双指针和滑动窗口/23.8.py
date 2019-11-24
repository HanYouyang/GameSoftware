def bruteforce(nums, k):
    count = 0
    for i in range(len(nums)):
        product = 1
        for j in range(i, len(nums)):
            product *= nums[j]
            if product >= k: break
            count += 1
    return count