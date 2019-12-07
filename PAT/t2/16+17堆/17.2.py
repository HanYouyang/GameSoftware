def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heapq.heappop(heap)

def findKthLargest2(nums, k):
    return heapq.nlargest(k, nums)[k - 1]

