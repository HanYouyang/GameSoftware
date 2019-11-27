def maxProfits(prices):
    maxProfit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            maxProfit = prices[i] - prices[i - 1]
    return  maxProfit

def maxProfits2(prices):
    maxProfit = 0
    for i in range(1, len(prices)):
        maxProfit += max(0, prices[i] - prices[i - 1])
    return maxProfit