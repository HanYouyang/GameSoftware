# 从前往后同时走 一块一慢
# when增加边界/移动指针
# valid合法窗口

# 1.1 从排序数组删除重复出现的数字
# 每个元素都最多重复一次 返回长度
# 有趣的是不停移动j的时候对i要相同就移动不同就修改（估计就是不停修改）
def removeDuplicates(alist):
    if not alist:
        return 0

    tail = 0

    for j in range(1, len(alist)):
        if alist[j] != alist[tail]:
            tail += 1
            alist[tail] = alist[j]

    return tail + 1

# 1.2 从排序数组删除重复出现的数字
# 1.dict去做
# 2.其实只需要上面修改比较前两个的内容
# 如果是3个的话边际条件判断更复杂一些
def removeDuplicates2(nums):
    count = 0
    for i in range(len(nums)):
        if count < 2 or nums[count - 2] != nums[i]:
            nums[count] = nums[i]
            count += 1
    return count

# 2 删除元素
# 1.根据现在的把后面元素放前面
# 2.把元素放后面
def removeElement(nums, val):
    i = 0
    for j in range(len(nums)):
        if nums[j] != val:
            nums[i] = nums[j]
            i += 1
    return i
def removeElement2(nums, val):
    start, end = 0, len(nums) - 1
    while start <= end:
        if nums[start] == val:
            nums[start], end = nums[end], end - 1
        else:
            start += 1
    return start

# 3 最大子序列均值
# k长度固定
# 1.accumulate出来数组用以计算/累进所有去减
# 2.用i和i+k之间不断前进计算
def findMaxnumsverage1(nums, K):
    P = [0]
    for x in nums:
        P.append(P[-1] + x)

    movingSum = max(P[i+K] - P[i] 
             for i in range(len(nums) - K + 1))
    return movingSum / float(K)

def findMaxnumsverage2(nums, K):
    movingSum = 0.0
    for i in range(K):
        movingSum += nums[i]
    res = movingSum
    for i in range(K, len(nums)):
        movingSum += nums[i] - nums[i - K]
        res = max(res, movingSum)
    return res / K

# 4 最大递增子序列
# 不断比较大小记录count
def findLengthOfLCIS(nums):
    result, count = 0, 0
    for i in range(len(nums)):
        if i == 0 or nums[i - 1] < nums[i]:
            count += 1
            result = max(result, count)
        else:
            count = 1
    return result

# 5 最短子数列符合条件和
# 定义满足条件就i移动否则移动j
def minsubarray(alist, target):
    if len(alist) == 0:
        return 0
    
    i = j = sums = 0
    minimum = sys.maxsize
    
    while j < len(alist):
        sums += alist[j]
        j += 1
        while sums >= target:
            minimum = min(minimum, j - i)
            sums -= alist[i]
            i += 1
    return 0 if min == sys.maxsize else minimum

# 6 找子串
# 1.find
# 2.找到后锁住不断比较
def strStr(haystack, needle):
    if len(haystack) < len(needle): 
        return None
    l1 = len(haystack)
    l2 = len(needle)
    for i in range(l1 - l2 + 1):
        count = 0
        while count < l2 and haystack[i + count] == needle[count]:
            count += 1
        if count == l2:
            return i
    return -1

# 7 连续数组乘积小于k
# Key在于计算自己子集，每个右边拓展的都和左边起始值构成子集
def bruteforce(nums, k):
    count = 0
    for i in range(len(nums)):
        product = 1
        for j in range(i, len(nums)):
            product *= nums[j]
            if (product >= k): break
            count += 1
    return count
def numSubarrayProductLessThanK(nums, k):
    product = 1
    i = 0
    ans = 0
    for j, num in enumerate(nums):
        product *= num
        while product >= k:
            product /= nums[i]
            i += 1
        ans += (j - i + 1)
    return ans

# 02
# 1.1 最长无重复子字符串
# 字符串就是说的滑动窗口子串
# 遇到重复移i，用dict查
# set存储idx，直接从新的j位置上把i调过去到idx + 1
# idx另外好处就是可以不用更新
def lengthOfLongestSubstring(s):
    start = maxLength = 0
    usedChar = {}

    for i, c in enumerate(s):
        if c in usedChar and start <= usedChar[c]:
            start = usedChar[c] + 1
        else:
            maxLength = max(maxLength, i - start + 1)
        usedChar[c] = i

    return maxLength
# 1.2 最长k重复子字符串
def lengthOfLongestSubstringKDistinct(s, k):
    start = 0
    longest = 0
    char_dict = {}

    for index in range(len(s)):
        char = s[index]
        char_dict[char] = char_dict.get(char, 0) + 1  # track count of chars
        # decrease the size of sliding window until you have k unique chars in sliding window
        while len(char_dict) > k: 
            char_dict[s[start]] -= 1
            if char_dict[s[start]] == 0:
                del char_dict[s[start]]
            start += 1
        longest = max(longest, index+1-start)

    return longest

# 2 最小包含元素子串长度
# 先找到第一个存在元素
# 用dict记录当前字母和次数
# 如果子串有重复也得找到内容
# 可以同时包括这些元素，是需要再去寻找的个数即可
import sys
def minWindow(s, t):
    if len(t) > len(s):
        return ""
    lt = len(t)
    count = lt
    ct = collections.Counter(t)
    left = 0
    right = 0
    minLength = sys.maxsize
    notfound = 1
    ansleft = 0
    ansright = 0
    print(ct)
    for i in range(len(s)):
        # found in t
        if ct[s[i]] > 0:
            count -= 1
        ct[s[i]] -= 1
        #print(s[i], ct)
        # found a window, containing all chars from t
        while count == 0:
            right = i
            notfound = 0
            if right - left < minLength:
                minLength = right-left
                ansleft = left
                ansright = right
            # when map[left] is 0, meaning the exit char is in t, then count++
            if ct[s[left]] == 0:
                count += 1
            ct[s[left]] += 1
            #print("left: ", s[left], ct)
            left += 1
    if notfound == 1:
        return ""
    return s[ansleft:ansright+1]

# 3 滑动窗口最大值
# 思路完全不同
def maxSlidingWindow(nums, k):
    d = collections.deque()
    out = []
    for i, n in enumerate(nums):
        while d and nums[d[-1]] < n:
            d.pop()
        d += i,
        if d[0] == i - k:
            d.popleft()
        if i >= k - 1:
            out += nums[d[0]]
    return out
