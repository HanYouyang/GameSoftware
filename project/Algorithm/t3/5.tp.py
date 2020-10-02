# 我们已经见过的Two Pointers相关的问题：
# Linked List: Find Middle Node
# Linked List: Determine Cycle
# Linked List: Find Cycle Start Point
# Linked List: Find kth Element From End
# Merge Sort
# Partition: Quick Sort, Find Kth Largest Element

# 1.单数组向后-滑动窗口
# 2.双数组向后
# 3.单数组一前一后
# 4.双数组向前

# 0 反转列表
# 1.用stack
# 2.相互交换
def reverse(nums):
    n = len(nums)
    for i in range(len(nums) // 2):# j = n - 1 - i
        nums[i], nums[n-1-i] = nums[n-1-i], nums[i]
    print(nums)

# 1 两数求和
# 1.1 dict 边找边存
def twoSum(nums, target):
    dic = {}
    for i, num in enumerate(nums):
        if num in dic:
            return [dic[num], i]
        else:
            dic[target - num] = i
# 1.2 双指针 排序 前后移动相加去依据比较结果移动
def twoSum2(num, target):
    index = []
    numtosort = num[:]; numtosort.sort()
    i = 0; j = len(numtosort) - 1
    while i < j:
        if numtosort[i] + numtosort[j] == target:
            for k in range(0,len(num)):
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

# 2 三数求和
# 三指针 排序 移动ijk
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

# 3 四数求和
# 3.1 四指针
def fourSum(num, target):
    num.sort(); res = []
    for i in range(len(num)):
        if i > 0 and num[i] == num[i - 1]: 
            continue 
        for j in range(i + 1 ,len (num)):
            if j > i + 1 and num[j] == num[j - 1]: 
                continue 
            l = j + 1
            r = len(num) - 1
            while l < r:
                sum = num[i] + num[j] + num[l] + num[r]
                if sum > target:
                    r -= 1
                elif sum < target:
                    l += 1
                elif l > j + 1 and num[l] == num[l - 1]:
                    l += 1
                elif r < len(num) - 1 and num[r] == num[r + 1]:
                    r -= 1
                else :
                    res.append([num[i],num[j],num[l],num[r]])
                    l += 1
                    r -= 1
    return res
# 3.2 简化为三数求和 用list每两个数字写出dict存储可能性 
def fourSum2(num, target):
    numLen, res, dict = len(num), set(), {}
    if numLen < 4: 
        return []
    num.sort()
    for p in range(numLen):
        for q in range(p+1 , numLen): 
            if num[p] + num[q] not in dict:
                dict[num[p] + num[q]] = [(p,q)]
            else :
                dict[num[p] + num[q]].append((p,q))
    for i in range(numLen):
        for j in range(i + 1, numLen - 2):
            T = target - num[i] - num[j]
            if T in dict:
                for k in dict[T]:
                    if k[0] > j: res.add((num[i], num[j], num [k[0]], num[k[1]]))
    return [list(i) for i in res]

# 4 k数求和
# 求每个子集的和 就看每个数字选还是不选 o2^n

# 5 合并两个有序数组
# 1.MergeSort 但需要额外空间 双指针两个都在前面
# 2.双指针两个都在后面比较依次给出放到最后
def merge(nums1, m, nums2, n):
    while m > 0 and n > 0:
        if nums1[m - 1] >= nums2[n - 1]:
            nums1[m + n - 1] = nums1[m - 1]
            m = m - 1
        else:
            nums1[m + n - 1] = nums2[n - 1]
            n = n - 1
    if n > 0:
        nums1[: n] = nums2[: n]

# 6 两有序数组最小元素差
# 移动i和j看谁目前是大的就移动另外一个
# 两列表同时从前往后
import sys
def printClosest(ar1, ar2):
    m = len(ar1)
    n = len(ar2)

    diff = sys.maxsize
    p1 = 0
    p2 = 0
    
    while (p1 < m and p2 < n):
        if abs(ar1[p1] - ar2[p2]) < diff:
            diff = abs(ar1[p1] - ar2[p2])

        if (ar1[p1] > ar2[p2]):
            p2 += 1
        else:
            p1 += 1
    return diff

# 7 两有序数组交集
# 1.二分搜索
# 2.双指针比较谁小就后移 相等放入新数组

# 8 连续子数组不超过m
# 此时都是正整数数组
# 找到左边界右边界寻找搜索判断的边界，维持局部最大和全局最大
# 注意非法的时候保存当前值判断是否为最大
# 另一方法是用accumulate计算当前值和之前所有值的和，最终得到数组减得差值
from itertools import accumulate
def maxSubarray(numbers, ceiling):
    cumSum = [0]
    cumSum = cumSum + numbers
    cumSum = list(accumulate(cumSum))

    l = 0
    r = 1 # two pointers start at tip of the array.
    maximum = 0
    while l < len(cumSum):
        while r < len(cumSum) and cumSum[r] - cumSum[l] <= ceiling:
            r += 1
        if cumSum[r - 1] - cumSum[l] > maximum: # since cumSum[0] = 0, thus r always > 0.
            maximum = cumSum[r - 1] - cumSum[l]
            pos = (l, r - 2)
        l += 1
    return pos
# 02
# 1 寻找子元素
# 出现次数超过半数
# 1.dict
# 2.排序后取正中间
# 3.扔掉两个不同的，剩下就两个就行，Moore投票算法
# 不停换count和换candidate，留下candidate就是
def majority(alist):
    result = count = 0
    for i in alist:
        if count == 0:
            result = i
            count = 1
        elif result == i:
            count += 1
        else:
            count -= 1
    return result

# 2 寻找子元素2
# 找超过三分之一的数字
# 还是得用Moore投票算法
# 过程较为复杂，但是可以记忆理解
def majority2(alist):
    n1 = n2 = None
    c1 = c2 = 0
    for num in alist:
        if n1 == num:
            c1 += 1
        elif n2 == num:
            c2 += 1
        elif c1 == 0:
            n1, c1 = num, 1
        elif c2 == 0:
            n2, c2 = num, 1
        else:
            c1, c2 = c1 - 1, c2 - 1
    size = len(alist)
    return [n for n in (n1, n2) 
               if n is not None and alist.count(n) > size / 3]

# 3 颜色排序
# 1.计数排序
# 2.用l和r两个指针与i比较
def sortColors(nums):
    count = [0] * 3
    for num in nums:
        count[num] += 1
    i = 0
    for j in range(3):
        for _ in range(count[j]):
            nums[i] = j
            i += 1

def sortColors2(nums):
    i, l, r = 0, 0, len(nums) - 1
    while i <= r:
        if nums[i] == 0:
            nums[i], nums[l] = nums[l], nums[i]
            i, l = i + 1, l + 1
        elif nums[i] == 2:
            nums[i], nums[r] = nums[r], nums[i]
            r -= 1
        else:
            i += 1

# 4 寻找k个最近元素
# 1.计算差并且排序
# 2.先找离得最近数字
def findClosestElements1(self, arr, k, x):
    diffTuples = sorted((abs(x - num), num) for num in arr)
    return sorted(map(lambda x: x[1], diffTuples[:k])) #prefer the smaller number for same diff.

def findClosestElements2(alist, k, x):
    left = right = bisect.bisect_left(alist, x)# l和r都用一个初始值来确保不会出问题
    while right - left < k:
        if left == 0: return alist[:k]
        if right == len(alist): return alist[-k:]
        if x - alist[left - 1] <= alist[right] - x: left -= 1
        else: right += 1
    return alist[left:right]

# 5 容纳最多的水
# 注意是挑选两根棍子和距离
# 相当于就是直接相向计算看内容，谁小移动谁
def maxArea(height):
    left = 0; right = len(height)-1
    res = 0
    while left < right:
        water = min(height[left], height[right]) * (right-left)
        res = max(res, water)
        if height[left] < height[right]: 
            left += 1
        else:
            right -= 1
    return res

# 6 雨水收集
# 两边同时向内运行，但是各边计算是用自己的，用高的减去低的
# 找到中间的峰值就移动右边的内容再去计算，总是用“峰值掐住”
def trapTP(height):
    if not height or len(height) < 3:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    ans = 0
    while (left < right):
        if (height[left] < height[right]):
            if height[left] >= left_max:
                left_max = height[left]  
            else:
                ans += (left_max - height[left])
            left += 1
        
        else:
            if height[right] >= right_max:
                right_max = height[right] 
            else:
                ans += (right_max - height[right])
            right -= 1
    return ans
