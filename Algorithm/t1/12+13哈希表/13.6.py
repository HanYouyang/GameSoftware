def containDup(nums):
    return len(nums) > len(set(nums))

def containDupInK(nums, k):
    dic = {}
    for i, v in enumerate(nums):
        if v in dic and i - dic[v] <= k:
            return True
        dic[v] = i
    return False