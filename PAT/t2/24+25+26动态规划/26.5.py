def knapSack(w, wt, val, n):
    k = [[0 for x in range(w + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(w + 1):
            if i == 0 or w == 0:
                k[i][w] = 0
            elif wt[i - 1] <= w:
                k[i][w] = max(val[i - 1] + k[i - 1][w - wt[i - 1]], k[i - 1][w])
            else:
                k[i][w] = k[i - 1][w]
    return k[n][w]
