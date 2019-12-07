import time

def count_sort(items):
    start = time.time()
    maxN, minN = items[0], items[0]
    for i in range(1, len(items)):
        if (items[i] > maxN): maxN = items[i]
        elif (items[i] < minN): minN = items[i]
    print(maxN)
    nums = maxN - minN + 1
    counts = [0] * nums

    for i in range(len(items)):
        counts[items[i] - minN] = counts[items[i] - minN] + 1
    
    pos = 0
    for i in range(nums):
        for j in range(counts[i]):
            items[pos] = i + minN
            pos += 1

    t = time.time() - start
    return len(nums), t