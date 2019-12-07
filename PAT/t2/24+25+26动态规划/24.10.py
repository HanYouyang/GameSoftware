def numDecoding(s):
    if s == '' or s[0] == 0:
        return 0
    dp = [1, 1]
    for i in range(2, len(s) + 1):
        result = 0
        if 10 <= int(s[i - 2 : i]) <= 26:
            result = dp[i - 2]
        if s[i - 1] != '0':
            result += dp[i - 1]
        dp.append(result)
    return dp[len(s)]