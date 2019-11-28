def maxProfits5(prices, k):
    if len(prices) < 2:
        return 0
    
    if len(prices) <= k / 2:
        maxProfitsTwo(prices)
    
    localprofit = [0] * (k + 1)
    globalProfit = [0] * (k + 1)

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        j = k
        while j > 0:
            localprofit[j] = max(globalProfit[j - 1], localprofit[j] + diff)
            globalProfit[j] = max(globalProfit[j], localprofit[j])
            j -= 1
    return globalProfit[k]