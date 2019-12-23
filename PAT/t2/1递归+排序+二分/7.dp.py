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
    return max(rob(nums[len(nums) != 1 :]), rob(nums[:-1]))

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
# 只要有正差就记录下来 不必在乎真实买卖过程
def maxProfit21(prices):
    max_profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            max_profit += prices[i] - prices[i - 1]
    return max_profit
def maxProfit22(prices):
    max_profit = 0
    for i in range(1, len(prices)):
        max_profit += max(0, prices[i] - prices[i - 1])
    return max_profit

# 1.3 买卖股票3
# 任意多次 每次交纳手续费
# 但此时要尽可能减少交易次数 所以最终两者都需要做成
# 今天的状态为两种，要么是买要么是卖，都求今天的最大值
# 今天 买就是昨天卖了或者昨天没动 今天卖就是昨天买了或者昨天没动
# 第一题也可以这么做
def maxProfit3(prices, fee):
    cash, hold = 0, -prices[0]
    for i in range(1, len(prices)):
        cash, hold = max(cash, hold + prices[i] - fee), max(hold, cash - prices[i])
    return cash

# 1.4 买卖股票4
# 进行两次交易 无手续费
# 可以进行拆分 从中间进行拆分 拆分较为繁琐
# 先从前往后看最大利润 再从后往前看最大利润
def maxProfit4(prices):
    total_max_profit = 0
    n = len(prices)
    left_profits = [0] * n
    min_price = float('inf')

    for i in range(n):
        min_price = min(min_price, prices[i])
        total_max_profit = max(total_max_profit, prices[i] - min_price)
        left_profits[i] = total_max_profit

    max_profit = 0
    max_price = float('-inf')
    for i in range(n - 1, 0, -1):
        max_price = max(max_price, prices[i])
        max_profit = max(max_profit, max_price - prices[i])
        total_max_profit = max(total_max_profit, max_profit + left_profits[i - 1])
    return total_max_profit

# 1.5 买卖股票5
# k次交易
# 用全局和局部两个值相互套用看最值
def maxProfit5(prices, k):
    if len(prices) < 2:
        return 0
    if len(prices) <= k / 2:
        maxProfit5(prices)

    local = [0] * (k + 1)
    globl = [0] * (k + 1)    
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        j = k
        while j > 0:
            local[j] = max(globl[j - 1], local[j] + diff)
            globl[j] = max(globl[j], local[j])
            j -= 1
    return globl[k]

# 1.6 买卖股票6
# 任意多次 卖出后要休息一天
# 对之前公式进行修改 也就意味着计算的过程i-2的内容
def maxProfit6(prices):
    if len(prices) < 2:
        return 0
    n = len(prices)
    sell = [0] * n
    buy  = [0] * n
    sell[0] = 0
    buy[0] = -prices[0]
    for i in range(1, n):
        sell[i] = max(sell[i - 1], buy[i - 1] + prices[i])
        buy[i] = max(buy[i - 1], (sell[i - 2] if i > 1 else 0) - prices[i])
            
    return sell[-1]

# 03 二维动态规划
# 1.1 独特路径
# 第一行和第一列是只有一种铺满就是向直走
# 后面的都是左上两格相加
# 优化绝大多数是给定算法时间复杂度优化空间流程
def uniquePaths1(m, n):
    aux = [[1 for x in range(n)] for x in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            aux[i][j] = aux[i][j - 1] + aux[i - 1][j]
    return aux[-1][-1]
def uniquePaths2(m, n):
    aux = [1 for x in range(n)]
    for i in range(1, m):
        for j in range(1, n):
            aux[j] = aux[j] + aux[j - 1]
    return aux[-1]

# 1.2 独特路径2
# 此时也是走不通就是设定为 后面也得设定为别的从上面走
def uniquePathsWithObstacles(obstacleGrid):
    M, N = len(obstacleGrid), len(obstacleGrid[0])
    dp = [1] + [0] * (N - 1)
    for i in range(M):
        for j in range(N):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[N - 1]

# 2 棋盘移动
# 找获利最大移动路线
# dp去做但是此时出发点多 表达状态+lookup
# 各个路径来到这个格子的最大值+本格值
def movingBoard1(board):
    result = board
    m = len(board)
    n = len(board[0])
    for i in range(1, m):
        for j in range (0, n):
            result[i][j] = max(0 if j == 0 else result[i - 1][j - 1], \
                               result[i - 1][j], \
                               0 if j == n - 1 else result[i - 1][j + 1] ) \
                            + board[i][j]
    return max(result[-1])
def movingBoard2(board):
    result = board[0]
    m = len(board)
    n = len(board[0])
    for i in range(1, m):
        for j in range (0, n):
            result[j] = max(0 if j == 0 else result[j-1], \
                            result[j], \
                            0 if j == n-1 else result[j+1] ) \
                        + board[j]
    return max(result)

# 3 最大正方形
# 找到正方形的时候还是会有重复计算
# 在遍历过程中也是计算如何取方块值与周边的关系
def maximalSquare(matrix):
    if matrix == []:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for x in range(m)]
    ans = 0
    for x in range(m):
        for y in range(n):
            dp[x][y] = int(matrix[x][y])
            if x and y and dp[x][y]:
                dp[x][y] = min(dp[x - 1][y - 1], dp[x][y - 1], dp[x - 1][y]) + 1
            ans = max(ans, dp[x][y])
    return ans * ans

# 4 0/1背包问题
# 每个珠宝不重样有重量和价值 书包有承重上限
# 1.子集穷举 o2^n 问题其实可以分割
# 2.分解问题状态 依次选择是抢还是不抢
# 状态数量都可以是抢还是不抢的乘积 但是依据重量列出情况 可能有重量限制
# 如果每个可以拿k个那就是不断更新值
def knapSack(W, wt, val, n):
    K = [[0 for x in range(W + 1)] for x in range(n+1)]
    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i - 1][w]
    return K[n][W]

# 5 最长公共子串
# 不要求连续但是有顺序
# 从后往前看是否相等可以降低问题难度 但是也是取两者之一往前的最值 
# 是看是否相等的矩阵判断后移动
def LCS(X, Y, m, n):
    matrix = [[0 for k in range(n + 1)] for l in range(m + 1)]
    result = 0
 
    for i in range(m + 1):
        for j in range(n + 1):
            if (i == 0 or j == 0):
                matrix[i][j] = 0
            elif (X[i - 1] == Y[j - 1]):
                matrix[i][j] = matrix[i - 1][j - 1] + 1
                result = max(result, matrix[i][j])
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])
    return result

# 6 最长递增子串
# 不要求连续
# 1.sort之后用上面题目的思路建立两个数组
# 2.DP虽然也暴力但是会存储起来 每个数字都自行比较前面所有数字
# 3.剪枝 如果前者保持1那本身小就可替代 实则bs替换数字后获得长度真值要再记录
def lengthOfLIS1(nums):
    sortNums = sorted(nums)
    n = len(nums)
    return LCS(nums, sortNums, n, n)
def lengthOfLIS2(nums):
    if not nums:
        return 0
    dp = [1]*len(nums)
    for i in range (1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
def lengthOfLIS3(nums):
    def search(temp, left, right, target):
        if left == right:
            return left
        mid = left + (right - left) // 2
        return search(temp, mid + 1, right, target) if temp[mid]<target else search(temp, left, mid, target)
    temp = []
    for num in nums:
        pos = search(temp, 0, len(temp), num)
        if pos >= len(temp):
            temp.append(num)
        else:
            temp[pos] = num
    return len(temp)
from bisect import bisect 
def lengthOfLIS4(nums):
    temp = []
    for num in nums:
        pos = bisect(temp, num) 
        if pos >= len(temp):
            temp.append(num)
        else:
            temp[pos] = num
    return len(temp)

# 7 矩阵乘法链
# 实则卡特兰树
# 对矩阵拆分的方法得出计算结果不断相加获得上面的值