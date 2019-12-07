# 56.合并区间 = 5.10
class Solution(object):
    def merge(self, intervals):
        # intervals = sorted(intervals, key= compare)
        intervals.sort(key = lambda x: x[0])
        merged = []
        for interval in intervals:
        	if not merged or merged[-1][1] < interval[0]:
        		merged.append(interval)
        	else:
        		merged[-1][1] = max(merged[-1][1], interval[1])
        return merged


# 57.插入区间 = 5.11
class Solution(object):
    def insert(self, intervals, newInterval):
        
        result = []
        for interval in intervals:
        	if newInterval[0] > interval[1]:
        		result.append(interval)
        	elif newInterval[1] < interval[0]:
        		result.append(newInterval)
        		newInterval = interval
        	elif newInterval[0] <= interval[1] or newInterval[1] >= interval[0]:
                newIntervalFirst = min(newInterval[0], interval[0])
                newIntervalSecond = max(interval[1], newInterval[1])
                newInterval = [newIntervalFirst, newIntervalSecond]               

        result.append(newInterval)
       	return result

# 75.红白蓝 = 22.9
# 重复值多数量少可以用count sort去做
# 先计数再排序
# def sortColors(nums):
#     count = [0] * 3
#     for num in nums:
#         count[num] += 1
#     i = 0 
#     for j in range(3):
#         for _ in range(count[j]):
#             nums[i] = j
#             i += 1
def sortColors(nums):
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


# 上面是数组，下面是链表
# 147.插入排序链表 = 9.5
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution(object):
    def insertionSortList(self, head):
        if not head:
        	return None

        dummy = ListNode(0)
        cur = head

        while cur is not None:
            pre = dummy
            while pre.next is not None and pre.next.val < cur.val:
                pre = pre.next
            temp = cur.next
            cur.next = pre.next
            pre.next = cur
            cur = temp
        return dummy.next

# 148.排序链表 = 9.6
# 此处是nlgn的速度排序并且注意函数在内部调用要使用self.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution(object):
    def getMiddle(self, head):
        if head is None:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow
    def merge(self, lHead, rHead):
        dummyNode = dummyHead = ListNode(0)
        while lHead and rHead:
            if lHead.val < rHead.val:
                dummyHead.next = lHead
                lHead = lHead.next
            else:
                dummyHead.next = rHead
                rHead = rHead.next
            dummyHead = dummyHead.next
        if lHead:
            dummyHead.next = lHead
        elif rHead:
            dummyHead.next = rHead
        return dummyNode.next
    
    def sortList(self, head):
        if head is None or head.next is None:
            return head
        mid = self.getMiddle(head)
        rHead = mid.next
        mid.next = None
        return self.merge(self.sortList(head), self.sortList(rHead))

# 164.排序 
# 有桶排序方法可以继续写
# 不要因为人家写是hard你就以为不能做
class Solution(object):
    def maximumGap(self, nums):

        if len(nums) < 2:
            return 0

        nums.sort()
        pre = nums[0]
        max_gap = float("-inf")

        for i in nums:
            max_gap = max(max_gap, i - pre)
            pre = i
        return max_gap

# 179.最大数
class Solution(object):
    def largestNumber(self, nums):
    	nums = [str(num) for num in nums]
    	nums.sort(cmp = lambda x, y : cmp(y+x, x+y))
    	return ''.join(nums).lstrip("0") or "0"

