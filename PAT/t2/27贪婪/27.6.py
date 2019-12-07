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