# 完全平衡树 用数组显示 parent and child (n - 1)//2
# 上面是最大值
# 构造 放入元素大与parent则往上移动


# 1.1 Kth Largest Element in Arary
# 找第k大就尝试用堆 维持size为k 但是注意找最大用minHeap 找最小用maxHeap
# 排序的partition算法是On更快 此处Onlgk
import heapq  
# O(k+(n-k)lgk) time, min-heap        
def findKthLargest(nums, k):
    return heapq.nlargest(k, nums)[k-1]
# O(k+(n-k)lgk) time, min-heap
def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heapq.heappop(heap)


# 1.2 Kth Largest Element in Arary
# 词频 用dict统计出来
# 1.构建类用排序算法标准 自行写出来所有内容
# 2.简便算法就是counter.most_common
def topKFrequent(nums, k):
    from collections import Counter as ct
    return [k for (k,v) in ct(nums).most_common(k)]

import collections
import heapq
import functools

@functools.total_ordering
class Element:
    def __init__(self, count, word):
        self.count = count
        self.word = word
        
    def __lt__(self, other):
        if self.count == other.count:
            return self.word > other.word
        return self.count < other.count
    
    def __eq__(self, other):
        return self.count == other.count and self.word == other.word

def topKFrequent(words, k):
    counts = collections.Counter(words)   

    freqs = []
    heapq.heapify(freqs)
    for word, count in counts.items():
        heapq.heappush(freqs, (Element(count, word), word))
        if len(freqs) > k:
            heapq.heappop(freqs)

    res = []
    for _ in range(k):
        res.append(heapq.heappop(freqs)[1])
    return res[::-1]


# 1.3 Ugly Number
# 判断条件需要改进
def uglyNumber(num):
    for p in 2, 3, 5:
        while num % p == 0 < num:
            num /= p
    return num == 1


# 1.4 Ugly Number II
# 先放进去再取 用heap取
# 放进去用235依次去乘这些数构成池子 依次放进去
# 就是每次生成太多但是装进来少
def nthUglyNumber(n):
    q2, q3, q5 = [2], [3], [5]
    ugly = 1
    for u in heapq.merge(q2, q3, q5):
        if n == 1:
            return ugly
        if u > ugly:
            ugly = u
            n -= 1
            q2 += 2 * u,
            q3 += 3 * u,
            q5 += 5 * u,


# 1.5 Find K Pairs with Smallest Sums
# 先构建最小值为基础对另外组k个元素的k个堆 然后用不停往里面加其他k元素的组合
# O(kLogk) 
def kSmallestPairs(nums1, nums2, k):
    queue = []
    def push(i, j):
        if i < len(nums1) and j < len(nums2):
            heapq.heappush(queue, [nums1[i] + nums2[j], i, j])
    push(0, 0)
    pairs = []
    while queue and len(pairs) < k:
        _, i, j = heapq.heappop(queue)
        pairs.append([nums1[i], nums2[j]])
        push(i, j + 1)
        if j == 0:
            push(i + 1, 0)
    return pairs
def kSmallestPairs2(nums1, nums2, k):
    queue = []
    def push(i, j):
        if i < len(nums1) and j < len(nums2):
            heapq.heappush(queue, [nums1[i] + nums2[j], i, j])
    for i in range(0, k):
        push(i, 0)
    pairs = []
    while queue and len(pairs) < k:
        _, i, j = heapq.heappop(queue)
        pairs.append([nums1[i], nums2[j]])
        push(i, j + 1)
    return pairs


# 2.1 Merge K Sorted List
# 注意是ll 可以分治两两合并
# 此处用heap暂存几个元素 用到哪个往后放
from queue import PriorityQueue
from LinkedList import LinkedList
from LinkedList import Node

def mergeKLists(lists):
    dummy = Node(None)
    curr = dummy
    q = PriorityQueue()
    for node in lists:
        if node: 
            q.put((node.value, node))
    while q.qsize()>0:
        curr.next = q.get()[1]
        curr = curr.next
        if curr.next: q.put((curr.next.value, curr.next))
    return dummy.next


# 2.2 Find Median from Data Stream
# 维护两个heap一个max一个min 用两个顶端值进行计算中位数
# 先看值的比较情况往哪里放 但是要维护两者差值不能太大
from heapq import *

class MedianFinder:
    def __init__(self):
        self.heaps = [], []

    def addNum(self, num):
        small, large = self.heaps
        heappush(small, -heappushpop(large, num))
        if len(large) < len(small):
            heappush(large, -heappop(small))

    def findMedian(self):
        small, large = self.heaps
        if len(large) > len(small):
            return float(large[0])
        return (large[0] - small[0]) / 2.0


# 2.3 Manage Your Project (IPO)
# 负值为了将maxHeap 变成minHeap
import heapq
def findMaximizedCapital(k, W, Profits, Capital):
    pqCap = []
    pqPro = []
    
    for i in range(len(Profits)):
        heapq.heappush(pqCap, (Capital[i], Profits[i]))
        
    for i in range(k):
        while len(pqCap) != 0 and pqCap[0][0] <= W:
            heapq.heappush(pqPro, -heapq.heappop(pqCap)[1])
        if len(pqPro) == 0:
            break
        W -= heapq.heappop(pqPro)
    return W

def findMaximizedCapital2(k, W, Profits, Capital):
    current = []
    future = sorted(zip(Capital, Profits))[::-1]
    for _ in range(k):
        while future and future[-1][0] <= W:  # afford
            heapq.heappush(current, -future.pop()[1])
        if current:
            W -= heapq.heappop(current)
    return W


# 总结各种数据结构