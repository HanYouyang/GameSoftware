def findMaxCaptial2(k, w, profits, captial):
    curr = []
    future = sorted(zip(captial, profits))[ : : -1]
    for _ in range(k):
        while future and future[-1][0] <= w:# 计算的是p最大下的c
            heapq.heappush(curr, -future.pop()[1])
        if curr:
            w += heapq.heappop(curr)
    return w