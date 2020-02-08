def maxProfits3(prices, fee):
    cash, hold = 0, -prices[0]
    for i in range(1, len(prices)):
        cash, hold = max(cash, hold + prices[i] - fee), max(hold, cash - prices[i])
    return cash