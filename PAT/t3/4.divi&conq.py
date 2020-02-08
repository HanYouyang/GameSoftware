# 01
# 1 快速算指数x^n
# 斐波那契矩阵计算左下角和右上角两个值可以olgn算递推结果
def fastPower(x, n):
    if n == 0:
        return 1.0
    elif n < 0:
        return 1 / fastPower(x, -n)
    elif n % 2:
        return fastPower(x * x, n // 2) * x
    else:
        return fastPower(x * x, n // 2)

# 2 搜索峰值
# 返回任意一个峰值
def searchPeak(alist):
    return peakHelper(alist, 0, len(alist) - 1)

def peakHelper(alist, start, end):
    if start == end:
        return start
    
    if (start + 1 == end):
        if alist[start] > alist[end]:
            return start
        return end
    
    mid = (start + end) // 2
    if alist[mid - 1] < alist[mid]and alist[mid] > alist[mid + 1]:
        return mid
    if alist[mid - 1] > alist[mid] and alist[mid] > alist[mid + 1]:
        return peakHelper(alist, start, mid - 1)
    return peakHelper(alist, mid + 1, end) # 四种情况第一个返回剩下三种要么向左要么向右

# 3.1 查找中值
# 快排一轮的结果就是找到某个数字在数组中的位置
# 利用这个位置跟k比较寻找你下一步要排序的值
# O(n) time, quick selection
def findKthSmallest(nums, k):
    if nums:
        pos = partition(nums, 0, len(nums) - 1)
        if k > pos + 1:
            return findKthSmallest(nums[pos + 1 :], k - pos - 1)
        elif k < pos + 1:
            return findKthSmallest(nums[: pos], k)
        else:
            return nums[pos]
# choose the right-most element as pivot   
def partition(nums, l, r):
    low = l
    while l < r:
        if nums[l] < nums[r]:
            nums[l], nums[low] = nums[low], nums[l]
            low += 1
        l += 1
    nums[low], nums[r] = nums[r], nums[low]
    return low

# 3.2 找第k大数字
# O(n) time, quick selection
def findKthLargest(nums, k):
    # convert the kth largest to smallest
    rst = findKthSmallest(nums, len(nums) + 1 - k)
    return rst


# 4 两数组交集
# 做法很多：set交集/sort+bs/sort+twoPointers
# 输出不含重复

# 5 两数组交集2
# 输出含重复
# 用prev存储上个交集的位置只要位置不同就加入

# 6 计算逆序对
# i < j and a[i] > a[j]
# 本身不为了排序，但是在分治的merge过程中不断进行判断得到大小
def merge(left, right):
    result = list()
    i, j = 0, 0
    inv_count = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        elif right[j] < left[i]:
            result.append(right[j])
            j += 1
            inv_count += (len(left) - i)
    result += left[i :]
    result += right[j :]
    return result, inv_count

def countInvFast(array):
    if len(array) < 2:
        return array, 0
    middle = len(array) // 2
    left, inv_left = countInvFast(array[: middle])
    right, inv_right = countInvFast(array[middle :])
    merged, count = merge(left, right)
    count += (inv_left + inv_right)
    return merged, count

# 7 已排序数组找到多余值
# olgn就是二分，已排序就是二分
# mid对应两个序列进行判断，index成为mid
def findExtraFast(arr1, arr2):
    index = 0
    left, right = 0, len(arr2) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr1[mid] == arr2[mid]:
            left = mid + 1
        else:
            index = mid
            right = mid - 1
    return index

# 8.1 最大子序列和
# 有负数
# 局部最大值不可能是负的，以此规避起始点
# dp的算法就是递推公式最简单on
# dc的算法就是onlgn
# 迭代左右但是中间分别有两个左右并记和，最终获取三值中最大者
def subarrayDC(alist):
    return subarrayDCHelper(alist, 0, len(alist)-1)

def subarrayDCHelper(alist, left, right):
    if (left == right):
        return alist[left]
    mid = (left + right) // 2
    return max(subarrayDCHelper(alist, left, mid), 
               subarrayDCHelper(alist, mid+1, right), 
               maxcrossing(alist, left, mid, right))

def maxcrossing(alist, left, mid, right):
    sum = 0
    leftSum = -sys.maxsize
    for i in range (mid, left - 1, -1):
        sum += alist[i]
        if (sum > leftSum):
            leftSum = sum
            
    sum = 0
    rightSum = -sys.maxsize
    for i in range (mid + 1, right + 1):
        sum += alist[i]
        if (sum > rightSum):
            rightSum = sum        

    return leftSum + rightSum


# 8.2 最大子序列和
def subarrayDP(alist):
    result = -sys.maxsize
    local = 0
    for i in alist:
        local = max(local + i, i)
        result = max(result, local)
    return result

# 9 芯片判断
# 找到第一个好芯片
# 因为对半分就是两个两个去判断，只留同真同假，剩到2个

# 10 快速整数乘法
# 卡拉楚巴算法
def karatsuba(x, y):
    """Function to multiply 2 numbers in a more efficient manner than the grade school algorithm"""
    if len(str(x)) == 1 or len(str(y)) == 1:
        return x * y
    else:
        n = max(len(str(x)), len(str(y)))
        nby2 = n // 2

        a = x // 10 ** (nby2)
        b = x % 10 ** (nby2)
        c = y // 10 ** (nby2)
        d = y % 10 ** (nby2)

        ac = karatsuba(a, c)
        bd = karatsuba(b, d)
        adPlusbc = karatsuba(a + b, c + d) - ac - bd
        # this little trick, writing n as 2*nby2 takes care of both even and odd n
        prod = ac * 10 ** (2 * nby2) + (adPlusbc * 10 ** nby2) + bd

        return prod

# 11 多项式乘法的快速傅里叶变换
def mults(A, B):
    m, n = len(A), len(B)
    result = [0] * (m + n - 1)
    for i in range (m):
        for j in range(n):
            result[i + j] += A[i] * B[j]
    return result

def printPoly(poly):
    n = len(poly)
    show = ""
    for i in range(n - 1, -1, -1):
        show += str(poly[i])
        if i != 0:
            show = show + "x^" + str(i)
        if i != 0:
            show = show + " + "
    print(show)

# 12.1 最近的点
# 1.排序后遍历
# 2.二分法加上分割的空间左右距离找最小

# 12.2 最近的点2
# 2D的也是同样思路中间划分，两边再从中间找
# 注意中间也是判断的情况可以从一个部分内找到
# x轴比如当下先选出来的min(l, r)的值作为半径去找范围内预计是3到4个点
# y也是排序的给出个d看加减范围内的值

# 13 水槽问题
# 实则是列出数字关系后，用二次组看不等式得根
# 开始减少到结束的天数算作i，使用计算总量的方式
# 结束那天是补上的水l和总量的水一起被用完
# Utility method to get
# sum of first n numbers
def getCumulateSum(n):
    return (n * (n + 1)) // 2

# Method returns minimum number of days
# after  which tank will become empty
def minDaysToEmpty(C, l):
 
    # if water filling is more than 
    # capacity then after C days only
    # tank will become empty
    if (C <= l) : return C 
 
    # initialize binary search variable
    lo, hi = 0, 1e4
 
    # loop until low is less than high
    while (lo < hi): 
        mid = int((lo + hi) / 2)
 
        # if cumulate sum is greater than (C - l) 
        # then search on left side
        if (getCumulateSum(mid) >= (C - l)): 
            hi = mid
         
        # if (C - l) is more then 
        # search on right side
        else:
            lo = mid + 1   
     
    # Final answer will be obtained by 
    # adding l to binary search result
    return (l + lo)

# 13.2 水槽问题二次方程法
import math
def solve(a, b, c):
    r = pow(b, 2) - 4 * a * c
    if (r < 0):
        raise ValueError("No Solution") 
    return (-b + math.sqrt(r)) / (2 * a)

def minDaysToEmpty(C, l):
    co = -2 * (C - l)
    return  math.ceil(solve(1, 1, co)) + l

# 14 奇偶数换序
# a1 a2 b1 b2变a1 b1 a2 b2
# 1.bf依次往前走
# 2.交换mid往左往右
def shufleArray(a, left, right):
     
    # If only 2 element, return
    if (right - left == 1):
        return
 
    # Finding mid to divide the array
    mid = (left + right) // 2
 
    # Using temp for swapping first
    # half of second array
    temp = mid + 1
 
    # Mid is use for swapping second
    # half for first array
    mmid = (left + mid) // 2
 
    # Swapping the element
    for i in range(mmid + 1, mid + 1):
        (a[i], a[temp]) = (a[temp], a[i])
        temp += 1
 
    # Recursively doing for 
    # first half and second half
    shufleArray(a, left, mid)
    shufleArray(a, mid + 1, right)

# 15 最少步数收集所有硬币
# 先找最小值，横着拿三次
# 肯定有依次全拿的方式
# 再就是先找到最小值拿到底下，然后左右两边取，递归这个过程
def minSteps(height):
    return minStepHelper(height, 0, len(height), 0)    
def minStepHelper(height, left, right, h):
    if left >= right:
        return 0
    
    m = left
    for i in range(left, right):
        if height[i] < height[m]:
            m = i
        
    return min(right - left, 
                minStepHelper(height, left, m, height[m]) +
                minStepHelper(height, m + 1, right, height[m]) +
                height[m] - h)

# 16 铺瓷砖
# 问题如果规模较大解决不了可以看看规模较小的
# 如果某个位置已经铺上那么周围就是不断围着铺好