def minCoins(v):
    available = [1, 2, 5, 10, 20, 50, 100, 500, 1000]
    result = []
    for i in available[: : -1]:
        while v >= i:
            v -= i
            result.append(i)
    return result