def comb(nums, t):
    result = []
    tmp = []
    combHelper(result, tmp, nums, t, 0)
    return result

def combHelper(result, tmp, nums, remains, start):
    if remains < 0: return
    if remains == 0:
        result.append(tmp[ : ])
    else:
        for i in range(start, len(nums)):
            tmp.append(nums[i])
            combHelper(result, tmp, nums, remains - nums[i], i)
            tmp.pop()            