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