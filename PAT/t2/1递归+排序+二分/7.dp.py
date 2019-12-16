# 动态规划和线性规划不同
# 分治法从上到下，动态规划从下到上（递推公式）实则拆分+查找

# 一维动态规划
# 1 数字表示
def coin(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = dp[2] = 1
    dp[3] = 2
    for i in range(4, n + 1):
        dp[i] = dp[i - 1] + dp[i - 3] + dp[i - 4]

    return dp[n]

# 2.1 入室抢劫
# 只能找隔着的房子
# 1.从下往上看的时候有递推的公式
# 2.进一步简化就是发现公式后直接不保存数组获得最后的值
def rob1(nums):
    n = len(nums)
    dp = [ [0] * 2 for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1]) # forget it
        dp[i][1] = nums[i - 1] + dp[i - 1][0]       # let's do it
    return max(dp[n][0], dp[n][1])  
def rob2(nums):
    yes, no = 0, 0
    for i in nums: 
        no, yes = max(no, yes), i + no
    return max(no, yes)

# 2.2 入室抢劫2
# 环形房间安排
# 如果抢劫第一个房子就相当于n不能抢只能到n-1
# 注意此时的输入还是数组不是环形链表
def rob3(nums):
    if len(nums) == 0:
        return 0
    if len(nums) == 1:
        return nums[0]

    return max(robRange(nums, 0, len(nums) - 1),\
               robRange(nums, 1, len(nums)))
def robRange(nums, start, end):
    yes, no = nums[start], 0
    for i in range(start + 1, end): 
        no, yes = max(no, yes), i + no
    return max(no, yes)

def rob4(nums):
    def rob(nums):
        yes, no = 0, 0
        for i in nums: 
            no, yes = max(no, yes), i + no
        return max(no, yes)
    return max(rob(nums[len(nums) != 1:]), rob(nums[:-1]))

# 2.3 抢劫聚会
# 抢一层就不能抢上下层
# 从叶子开始分析往上走
# 还需要自己设计adt，node放到dict里面去，set里面存leaf

# 3 瓷砖问题
# 计算铺瓷砖的方式
# 实则就是斐波那契数列
# 1.on的数组遍历
# 2.lgn的矩阵相乘

# 4 最小台阶问题
# 还是递推需要理解内容上取最小值
def minCostClimbingStairs(cost):
    n = len(cost) + 1
    dp = [0] * n
    for i in range(2, n):
        dp[i] = min(dp[i - 2] + cost[i - 2], dp[i - 1] + cost[i - 1])
    return dp[n - 1]

def minCostClimbingStairs2(cost):
    dp0, dp1, dp2 = 0, 0, 0
    for i in range(2, len(cost) + 1):
        dp2 = min(dp0 + cost[i - 2], dp1 + cost[i - 1])
        dp0, dp1 = dp1, dp2
    return dp2

# 5 解码方式
# 类似去看如何找到合适的解读方式不至于读错
# 实则是加上判断条件的斐波那契
# 程序写的时候是回顾的方式处理字符串
def numDecodings(s):
    if s == "" or s[0] == '0': return 0
    dp = [1, 1]
    for i in range(2, len(s) + 1):
        # if it is 0, then dp[i] = 0
        result = 0
        if 10 <= int(s[i - 2: i]) <= 26:
            result = dp[i - 2]
        if s[i - 1] != '0':
            result += dp[i - 1]
        dp.append(result)
    return dp[len(s)]

# 6 独特二叉树的搜索路径
# 问多少种构造方式 卡特兰树 通项是乘积公式 计算结果是阶乘相除
def numTress(n):
    if n <= 2:
        return n
    sol = [0] * (n + 1)
    sol[0] = sol[1] = 1
    for i in range(2, n + 1):
        for left in range (0, i):
            sol[i] += sol[left] * sol[i - 1 - left]
    return sol[n]   

# 7 最大子序列乘积
# 还是要记录局部最大值，再记录局部最小值为的是避免出现负负得正
def maxProduct(nums):
    if len(nums) == 0:
        return 0
    maximum = minimum = result = nums[0]
    for i in range(1, len(nums)):
        maximum, minimum = max(maximum * nums[i], minimum * nums[i], nums[i]), \
                           min(maximum * nums[i], minimum * nums[i], nums[i])
        result = max(result, maximum)
    return result

# 02
# 1.1 买卖股票
# 进行一次交易求最大利润
# 每次都更新最小值，同时更新的是当前利润值
def maxProfit11(prices):
    if len(prices) < 2:
        return 0
    minPrice = prices[0]
    maxProfit = 0
    for price in prices:
        if price < minPrice:
            minPrice = price
        if price - minPrice > maxProfit:
            maxProfit = price - minPrice
    return maxProfit
def maxProfit12(prices):
    if len(prices) < 2:
        return 0
    minPrice = prices[0]
    dp = [0] * len(prices)
    for i in range(len(prices)):
        dp[i] = max(dp[i-1], prices[i] - minPrice)
        minPrice = min(minPrice, prices[i])
    return dp[-1]

# 1.2 买卖股票2
# 任意多次 必须先买在卖
# 还是得找最小值再找差



