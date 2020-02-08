def generParen(n):
    return generate('', n, n)
def generate(prefix, left, right, parens = []):
    if right == 0: parens.append(prefix)
    if left > 0: generate(prefix + '(', left - 1, right)
    if right > left: generate(prefix + ')', left, right - 1)
    return parens

# N-Queens
def solveNQ(n):
    res = []
    dfs([- 1] * n, 0, [], res)
    return res
def dfs(nums, index, path, res):
    if index == len(nums):
        res.append(path)
        return
    for i in range(len(nums)):
        nums[index] = i
        if valid(nums, index):
            tmp = '.' * len(nums)
            dfs(nums, index + 1, path + [tmp[ : i] + 'Q' + tmp[i + 1: ]], res)
def valid(nums, n):
    for i in range(n):
        if abs(nums[i] - nums[n] == n - i or nums[i] == nums[n]):
            return False
    return True