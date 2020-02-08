def maxProfits(prices):
    if len(prices) < 2:
        return 0
    minPrice = prices[0]
    maxProfit = 0
    for price in prices:
        if price < minPrice:
            minPrice = price
        if price - minPrice > maxProfit:
            maxProfit = price - minPrice
    return maxProfit

def maxProfits2(prices):
    if len(prices) < 2:
        return 0
    minPrice = prices[0]
    maxProfit = 0
    for i in range(len(prices)):
        maxProfit = max(maxProfit, prices[i] - minPrice)
        minPrice = min(minPrice, prices[i])
    return maxProfit