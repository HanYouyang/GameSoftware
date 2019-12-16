# 02
# 1.1 Subset
# Given a set of distinct integers, nums, return all possible subsets
# 插入法+用到两处copy[:]（特用于Python）
def subsets(nums):
    result = [[]]
    for num in nums:
        for element in result[:]:
            x = element[:]
            x.append(num)
            result.append(x)
    return result
# 1.2 Subset回溯法
def subsetsRecursive(nums):
    lst = []
    result = []
    subsetsRecursiveHelper(lst, result, nums, 0)
    return result
def subsetsRecursiveHelper(lst, result, nums, pos):
    result.append(lst[:])
    for i in range(pos, len(nums)):
        lst.append(nums[i])
        subsetsRecursiveHelper(lst, result, nums, i + 1)
        lst.pop()
# 2.去除重复 All subsets
# 排序input后面再“剪枝”如果当前和刚才的相等就continue
def subsetsRecursive2(nums):
    lst = []
    result = []
    nums.sort()
    subsetsRecursiveHelper2(lst, result, nums, 0)
    return result
def subsetsRecursiveHelper2(lst, result, nums, pos):
    result.append(lst[:])
    for i in range(pos, len(nums)):
        if i != pos and nums[i] == nums[i - 1]:
            continue
        lst.append(nums[i])
        subsetsRecursiveHelper2(lst, result, nums, i + 1)
        lst.pop()
# 3.Permutation 排列组合
# 跟上面的区别在于不用去除之前的数字
def perm(result, nums):
    if len(nums) == 0:
        print(result)

    for i in range(len(nums)):
        perm(result + str(nums[i]), nums[0 : i] + nums[i + 1 :])
# 4.Permutation Unique
# 也是包含重复，也是要求不能出现重复
def permUnique(result, nums):
    nums.sort()
    if len(nums) == 0:
        print(result)

    for i in range(len(nums)):
        if nums[i] == nums[i - 1]:
            continue
        permUnique(result + str(nums[i]), nums[0 : i] + nums[i + 1 :])
# 5.Permutation of K
# 不选完所有nums元素那就是设定k个内容
def permSizeK(result, nums, k):
    if k == 0:
        print(result)

    for i in range(len(nums)):
        permSizeK(result + str(nums[i]), nums[0 : i] + nums[i + 1 :], k - 1)
# 6.Permutation of Letter
# 按照规则给出数字，要求目前结果如何
results = set()
keys = set()
def permLetter(word, rule):
    rule = rule.lower()
    for c in rule:
        keys.add(c)
    permLetterHelper(word, rule, 0, '')
def permLetterHelper(word, rule, index, prefix):
    for i in range(index, len(word)):
        c = word[i]
        if c in keys:
            permLetterHelper(word, rule, i + 1, prefix + c)
            c = c.upper()
            permLetterHelper(word, rule, i + 1, prefix + c)
        else:
            prefix += c
    if len(prefix) == len(word):
        results.add(prefix)
# 7.Combination/Any Sum
# 找subset的和为给定的值
def comb(nums, remains):
    tmp = []
    result = []
    combHelper(tmp, result, nums, remains, 0)
    return result
def combHelper(tmp, result, nums, remains, start):
    if remains < 0: return 
    if remains == 0:
        result.append(tmp[:])
    else:
        for i in range(start, len(nums)):
            tmp.append(nums[i])
            combHelper(tmp, result, nums, remains - nums[i], i + 1)
            tmp.pop()
# 8.Combination/Any Sum Unique
# 还是加限制条件还是之前的两个套路
def comb2(nums, remains):
    tmp = []
    result = []
    nums.sort()
    combHelper2(tmp, result, nums, remains, 0)
    return result
def combHelper2(tmp, result, nums, remains, start):
    if remains < 0: return 
    if remains == 0:
        result.append(tmp[:])
    else:
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            tmp.append(nums[i])
            combHelper2(tmp, result, nums, remains - nums[i], i + 1)
            tmp.pop()
# 9.Parentheses给出括号所有可能
def generateParentheses(n):
    return generate('', n, n)
def generate(written, left, right, parens = []):
    if right == 0:   parens.append(written)
    if left > 0:     generate(written + '(', left - 1, right)
    if right > left: generate(written + ')', left, right - 1)
    return parens