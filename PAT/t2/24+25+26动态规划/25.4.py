def maxProfits4(prices):
    totalMaxProfit = 0
    n = len(prices)
    leftProfit = [0] * n
    minPrice = float('inf')

    for i in range(n):
        minPrice = min(minPrice, prices[i])
        totalMaxProfit = max(totalMaxProfit, prices[i] - minPrice)
        leftProfit[i] = totalMaxProfit
    
    maxProfit = 0
    maxProfit = float('-inf')
    for j in range(n - 1, 0, -1):
        maxPrice = max(maxPrice, prices[j])
        maxProfit = max(maxProfit, maxPrice - prices[j])
        totalMaxProfit = max(totalMaxProfit, maxProfit + leftProfit[j - 1])
    return totalMaxProfit
