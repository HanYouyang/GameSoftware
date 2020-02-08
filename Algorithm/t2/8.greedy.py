# 贪心就是局部全取最优解
# 难点在如何证明
# 已经遇见的 dijkstra bellman-ford

# 1 找硬币
# 最少硬币找钱
# 每次用尽量多的 
def minCoins(V):
    available = [1, 2, 5, 10, 20, 50, 100, 500, 1000]
    result = []
    for i in available[: : -1]:
        while (V >= i):
            V -= i
            result.append(i)
    return result

# 2 活动集合 类似后面最小平台数
# 找到最多集合 使开始时间和结束时间不冲突
# 结束时间排序找最早 下个开始时间晚于结束时间即可
def printMaxActivities(acts):
    n = len(acts)
    sortActs = sorted(acts, key = lambda tup: tup[1])
    prev = sortActs[0]
    print(prev)
    for curr in sortActs:
        if curr[0] >= prev[1]:
            print(curr)
            prev = curr

# 3 最小数字和
# 给数字和位数求最小 
# 判断完了就是逆循环
def findSmallest(m, s):
    if (s == 0):
        if(m == 1) :
              print("Smallest number is 0") 
        else : 
              print("Not possible")
        return
    if (s > 9 * m):
        print("Not possible")
        return
    res = [0 for i in range(m + 1)]
    # deduct sum by one to account for cases later 
    # (There must be 1 left for the most significant digit)
    s -= 1
    for i in range(m - 1, 0, -1):
        # If sum is still greater than 9, digit must be 9.
        if (s > 9):
            res[i] = 9
            s -= 9
        else:
            res[i] = s
            s = 0# ？？？？
    res[0] = s + 1
    print("Smallest number is ", end = "")
    for i in range(m):
        print(res[i], end = "")

# 4 两数最小和
# 用堆速度比排序更快 建立ton 当然取用的时候还是tonlgn
import heapq
def minSum(a):
    heapq.heapify(a)
    num1 = 0
    num2 = 0
    while a:
        num1 = num1 * 10 + heapq.heappop(a)
        if a:
            num2 = num2 * 10 + heapq.heappop(a)
    return num1 + num2         

# 5 最低成本连接绳索
# 还是使用Heap再insert
import heapq
def ropeCost(ropes):
    heapq.heapify(ropes)
    total = 0
    while ropes:
        first = heapq.heappop(ropes)
        second = heapq.heappop(ropes)
        local = first + second
        total += local
        if not ropes:
            break
        heapq.heappush(ropes, local)
    return total  

# 6 最小平台数
# 用双指针对两个数组进行移动判断 实则Merge sort
def findPlatform(arr, dep, n):
    arr.sort()
    dep.sort()
    # plat_needed indicates number of platforms needed at a time
    plat_needed = 0
    result = 0
    i = 0
    j = 0
    # Similar to merge in merge sort to process all events in sorted order
    while (i < n and j < n):
        if (arr[i] < dep[j]):
            plat_needed += 1
            i += 1
            result = max(result, plat_needed)
        else:
            plat_needed -= 1
            j += 1
    return result

# 7 部分背包问题
# 需要计算性价比 从性价比排序后看到能否最高 要切割
def fracKnapsack(capacity, weights, values):
    numItems = len(values)
    valuePerWeight = sorted([[v / w, w, v] for v, w in zip(values, weights)], reverse = True)
    print(valuePerWeight)# 注意上面是从大到小
    totalCost = 0.
    for tup in valuePerWeight:
        if capacity >= tup[1]:
            capacity -= tup[1]
            totalCost += tup[2]
        else:
            totalCost += capacity * tup[0]
            break
    return totalCost

# 8 分蛋糕
# 每个人要求不同 使尽量多孩子满意
# 按照孩子需求排序 双指针移动

# 9 最小成本切割正方形
# 尽可能先切长边多的避免短边切更多刀 尽可能先切贵的
def minimumCostOfBreaking(X, Y, m, n):
    res = 0
    # sort the horizontal cost in reverse order
    X.sort(reverse = True)
    # sort the vertical cost in reverse order
    Y.sort(reverse = True)
    # initialize current width as 1
    hzntl = 1; vert = 1
    # loop untill one or both
    # cost array are processed
    i = 0
    j = 0
    while (i < m and j < n):
        if (X[i] > Y[j]):
            res += X[i] * vert
            # increase current horizontal
            # part count by 1
            hzntl += 1
            i += 1
        else:
            res += Y[j] * hzntl
            # increase current vertical
            # part count by 1
            vert += 1
            j += 1
    # loop for horizontal array, if remains
    total = 0
    while (i < m):
        total += X[i]
        i += 1
    res += total * vert
    #loop for vertical array, if remains
    total = 0
    while (j < n):
        total += Y[j]
        j += 1
    res += total * hzntl
    return res

# 10.1 交换得最小数组
# 得确定移动次数和k关系
# 如未排序在k+1范围内移动元素 已排序再往后移动
def minimizeWithKSwaps(arr, n, k):
    for i in range(n - 1):
        pos = i
        for j in range(i + 1, n):
            # If we exceed the Max swaps then terminate the loop
            if ( j - i > k):
                break
            # Find the minimum value from i+1 to max (k or n)
            if (arr[j] < arr[pos]):
                pos = j
        # Swap the elements from Minimum position we found till now to the i index
        for j in range(pos, i, -1):
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
        # Set the final value after swapping pos-i elements
        k -= pos - i

# 10.2 最小化极差
# 不知道中间数字如何增减所以遍历
def getMinDiff(arr, n, k):
    if (n == 1):
        return 0
    # Sort all elements
    arr.sort() 
    # Initialize result
    ans = arr[n - 1] - arr[0] 
    # Handle corner elements
    small = arr[0] + k 
    big = arr[n - 1] - k 
    if (small > big):
        small, big = big, small 
    # Traverse middle elements
    for i in range(1, n - 1):
        subtract = arr[i] - k 
        add = arr[i] + k 
        # If both subtraction and addition
        # do not change diff
        if (subtract >= small or add <= big):
            continue
        # Either subtraction causes a smaller
        # number or addition causes a greater
        # number. Update small or big using
        # greedy approach (If big - subtract
        # causes smaller diff, update small
        # Else update big)
        if (big - subtract <= add - small):
            small = subtract 
        else:
            big = add 
    return min(ans, big - small) 