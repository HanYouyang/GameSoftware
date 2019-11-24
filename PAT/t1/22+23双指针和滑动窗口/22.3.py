def twoSum(nums, target):
    dic = {}
    for i, num in enumerate(nums):
        if num in dic:
            return [dic[num], i]
        else:
            dic[target - num] = i

def twoSum2(num, target):
    index = []
    numtosort = num[:]; numtosort.sort()
    i = 0; j = len(numtosort) - 1
    while i < j:
        if numtosort[i] + numtosort[j] == target:
            for k in range(0, len(num)):
                if num[k] == numtosort[i]:
                    index.append(k)
                    break
            for k in range(len(num) - 1, -1, -1):
                if num[k] == numtosort[j]:
                    index.append(k)
                    break
            index.sort()
            break
        elif numtosort[i] + numtosort[j] < target:
            i = i + 1
        elif numtosort[i] + numtosort[j] > target:
            j = j - 1           
    return (index[0] + 1, index[1] + 1)


def threeSum(nums):
    res = []
    nums.sort()
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append((nums[i], nums[l], nums[r]))
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1; r -= 1
    return res

def fourSum(num, target):
    num.sort();res = []
    for i in range(len(num)):
        if i > 0 and num[i] == num[i - 1]:
            continue
        for j in range(i + 1, len(num)):
            if j > i + 1 and num[j] == num[j - 1]:
                continue
            l = j + 1
            r = len(num) - 1
            while l < r:
                sumAll = num[i] + num[j] + num[l] + num[r]
                if sumAll > target:
                    r -= 1
                elif sumAll < target:
                    l += 1
                elif l > j + 1 and num[l] == num[l - 1]:
                    l += 1
                elif r < len(num) - 1 and num[r] == num[r + 1]:
                    r -= 1
                else:
                    res.append([num[i], num[j], num[l], num[r]])
                    l += 1
                    r -= 1
    return res

def fourSum2(num, target):
    numLen, res, dic = len(num), set(), {}
    if numLen < 4:
        return []
    num.sort()
    for p in range(numLen):
        for q in range(p + 1, numLen):
            if num[p] + num[q] not in dic:
                dic[num[p] + num[q]] = [(p, q)]
            else:
                dic[num[p] + num[q]].append((p, q))
    for i in range(numLen):
        for j in range(i + 1, numLen - 2):
            T = target - num[i] - num[j]
            if T in dic:
                for k in dic[T]:
                    if k[0] > j:
                        res.add((num[i], num[j], num[k[0]], num[k[1]]))
    return [list(i) for i in res]