def maxProfit6(prices):
    if len(prices) < 2:
        return 0
    n = len(prices)
    sell = [0] * n
    buy = [0] * n
    sell[0] = 0
    buy[0] = -prices[0]
    for i in range(1, n):
        sell[i] = max(sell[i - 1], buy[i - 1] + prices[i])
        buy[i] = max(buy[i - 1], (sell[i - 2] if i > 1 else 0) - prices[i])
    
    return sell[-1]