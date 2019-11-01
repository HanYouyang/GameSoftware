def permUnique(result, nums):
    nums.sort()
    if (len(nums) == 0):
        print(result)
    for i in range(len(nums)):
        if (i != 0 and nums[i] == nums[i - 1]):
            continue
        permUnique(result + str(nums[i]), nums[0 : i] + nums[i + 1: ])

def permSizeK(result, nums, k):
    if k == 0:
        print(result)
    for i in range(len(nums)):
        permSizeK(result + str(nums[i]), nums[0 : i] + nums[i + 1: ], k - 1)

# 根据给出来的数字进行理解
results = set()
keys = set()
def permLetter(word, rule):
    rule = rule.lower()
    for c in rule:
        keys.add(c)
    permHelper(word, rule, 0, '')
def permHelper(word, rule, index, prefix):
    length = len(word)

    for i in range(index, length):
        c = word[i]
        if (c in keys):
            permHelper(word, rule, i + 1, prefix + c)

            c = c.upper()
            permHelper(word, rule, i + 1, prefix + c)
        else:
            prefix += c
    if (len(prefix) == len(word)):
        results.add(prefix)            