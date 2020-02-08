def perm(result, nums):
    if (len(nums) == 0):
        print(result)
    
    for i in range(len(nums)):
        perm(result + str(nums[i]), nums[0 : i] + nums[i + 1 : ])        

# 存储数据版本
def permute(nums):
    perms = [[]]
    for n in nums:
        new_perms = []
        for perm in perms:
            for i in range(len(perm) + 1):
                new_perms.append(perm[ : i] + [n] + perm[i : ])
        perms = new_perms
    return perms
    