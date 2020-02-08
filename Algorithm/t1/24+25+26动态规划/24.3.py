def rob(nums):
    n = len(nums)
    dp = [[0] * 2 for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1])
        dp[i][1] = nums[i - 1] + dp[i - 1][0]
    return max(dp[n][0], dp[n][1])

# 完全不看可能面对的前面的值，推到哪里就写到哪里
def rob2(nums):
    yes, no = 0, 0
    for i in nums:
        no, yes = max(no, yes), i + no
    return max(no, yes)
