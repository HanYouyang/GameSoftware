# 1 二分搜索
def binarySearcheIter(nums, target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        elif nums[mid] > target:
            right = mid - 1
        else:
            return mid
    return -1

# 2 二分搜索模板
# 三问排序/重复/负数
# 1.先判空确保l和r不会为负数
# 2.循环条件保证最终相邻/重叠
# 3.相等处设置是找第一个
# 4.对最终的相邻/重叠条件进行判断
def binarySearche(nums, target):
    # 已sort
    if len(nums) == 0:
        return -1

    left = 0
    right = len(nums) - 1
    while left + 1 < right:
        mid = left + (right - left) // 2
        if nums[mid] >= target:
            right = mid
        else: # nums[mid] < target:
            left = mid

    if nums[left] == target:
        return left
    if nums[right] == target:
        return right
    
    return - 1

# 3 旋转已排序数组查找最小值
# mid大于左半边的话就是排好序的半边
def searchLazy(alist):
    alist.sort()
    return alist[0]
def searchsLow(alist):
    mmin = alist[0]
    for i in alist:
        mmin = min(mmin, i)
    return mmin
def searchMin(alist):
    if len(alist) == 0:
        return -1    
    left, right = 0, len(alist) - 1
    while left + 1 < right: 
        if (alist[left] < alist[right]):
            return alist[left];
        mid = left + (right - left) // 2
        if (alist[mid] >= alist[left]):
            left = mid + 1
        else:
            right = mid
    return alist[left] if alist[left] < alist[right] else alist[right]

# 4 旋转数组中查指定值
def searchTarget(alist, target):
    if len(alist) == 0:
        return -1    
    left, right = 0, len(alist) - 1
    while left + 1 < right: 
        mid = left + (right - left) // 2
        if alist[mid] == target:
            return mid
        
        if (alist[left] < alist[mid]):
            if alist[left] <= target and target <= alist[mid]:
                right = mid
            else:
                left = mid
        else:
            if alist[mid] <= target and target <= alist[right]:
                left = mid
            else: 
                right = mid
                            
    if alist[left] == target:
        return left
    if alist[right] == target:
        return right
        
    return -1

# 5 寻找位置或插入
def searchInsertPosition(alist, target):
    if len(alist) == 0:
        return 0  

    left, right = 0, len(alist) - 1
    while left + 1 < right: 
        mid = left + (right - left) // 2
        if alist[mid] == target:
            return mid
        if (alist[mid] < target):
            left = mid
        else:
            right = mid
            
    if alist[left] >= target:
        return left
    if alist[right] >= target:
        return right

    return right + 1 # 找不到位置就放在最后

# 6 查重复数字的前后区间
# 找第一个就是>= target把mid作为right，找最后一个就是<= target把mid作为left
def searchRange(alist, target):
    if len(alist) == 0:
        return (-1, -1)  
    
    lbound, rbound = -1, -1

    # search for left bound 
    left, right = 0, len(alist) - 1
    while left + 1 < right: 
        mid = left + (right - left) // 2
        if alist[mid] == target:
            right = mid
        elif (alist[mid] < target):
            left = mid
        else:
            right = mid
            
    if alist[left] == target:
        lbound = left
    elif alist[right] == target:
        lbound = right
    else:
        return (-1, -1)

    # search for right bound 
    left, right = 0, len(alist) - 1        
    while left + 1 < right: 
        mid = left + (right - left) // 2
        if alist[mid] == target:
            left = mid
        elif (alist[mid] < target):
            left = mid
        else:
            right = mid
            
    if alist[right] == target:
        rbound = right
    elif alist[left] == target:
        rbound = left
    else:
        return (-1, -1)        
        
    return (lbound, rbound)

# 7 空字符隔开查找
# 此处就是找到right和mid把中间内容全部整理出来
def searchEmpty(alist, target):
    if len(alist) == 0:
        return -1

    left, right = 0, len(alist) - 1
    
    while left + 1 < right:
        while left + 1 < right and alist[right] == "":
            right -= 1
        if alist[right] == "":
            right -= 1
        if right < left:
            return -1
        
        mid = left + (right - left) // 2
        while alist[mid] == "":
            mid += 1
            
        if alist[mid] == target:
            return mid
        if alist[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    if alist[left] == target:
        return left
    if alist[right] == target:
        return right    
        
    return -1

# 8 数据流中查找
# 已经排序情况下翻倍寻找

# 02
# 1 供暖设备
# 先看每个房附近供暖设备的距离最小值，不是用供暖设备去找
# 最后找所有距离最小值的最大值
# bisect函数找到距离最近的大于该数的位置
from bisect import bisect
def findRadius(houses, heaters):
    heaters.sort()
    ans = 0

    for h in houses:
        hi = bisect(heaters, h)
        left = heaters[hi - 1] if hi - 1 >= 0 else float('-inf')
        right = heaters[hi] if hi < len(heaters) else float('inf')
        ans = max(ans, min(h - left, right - h))

    return ans

# 2.1 sqrt(x)
# 用二分的方式逼近当中要计算的那个值
def sqrt(x):
    if x == 0:
        return 0
    left, right = 1, x
    while left <= right:
        mid = left + (right - left) // 2
        if (mid == x // mid):
            return mid
        if (mid < x // mid):
            left = mid + 1
        else:
            right = mid - 1
    return right
# 2.2 牛顿法
def sqrtNewton(x):
    r = x
    while r * r > x:
        r = (r + x//r) // 2
    return r

# 3 矩阵搜索
# 排序好的矩阵去寻找
# 从左下角开始比较target

# 4 矩阵搜索2
# 找第k小的值，相应可以找个k大的值按照需要改造
from bisect import bisect
def kthSmallest(matrix, k):
    lo, hi = matrix[0][0], matrix[-1][-1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if sum(bisect(row, mid) for row in matrix) < k:
            lo = mid + 1
        else:
            hi = mid
    return lo

# 5 找到重复数
# 找到中间数看从0数个数是大于还是小于mid得到最终结果
def findDuplicate(nums):
    low = 0
    high = len(nums)

    while low < high:
        mid = low + (high - low) // 2
        count = 0
        for i in nums:
            if i <= mid:
                count += 1
        if count <= mid:
            low = mid + 1
        else:
            high = mid
    return low

# 6 地板和鸡蛋
# 要求每个区间摔碎鸡蛋的次数一致，那么就计算多少次