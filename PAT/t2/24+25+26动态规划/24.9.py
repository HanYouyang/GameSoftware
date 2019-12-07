def minCostClimb(cost):
    n = len(cost) + 1
    dp = [0] * n
    for i in range(2, n):
        dp[i] = min(dp[i - 2] + cost[i - 2], dp[i - 1] + cost[i - 1])
    return dp[n - 1]

def minCostClimb2(cost):
    dp0, dp1, dp2 = 0, 0, 0
    for i in range(2, len(cost) + 1):
        dp2 = min(dp0 + cost[i - 2], dp1 + cost[i - 1])
        dp0, dp1 = dp1, dp2
    return dp2
