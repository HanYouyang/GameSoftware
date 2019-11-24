def updateMatrix2(matrix):
    def DP(i, j, m, n, dp):
        if i > 0: dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)
        if j > 0: dp[i][j] = min(dp[i][j], dp[i][j - 1] + 1)
        if i < m - 1: dp[i][j] = min(dp[i][j], dp[i + 1][j] + 1)
        if j < n - 1: dp[i][j] = min(dp[i][j], dp[i][j + 1] + 1)
    
    if not matrix: return [[]]
    m, n = len(matrix), len(matrix[0])
    dp = [[0x7fffffff if matrix[i][j] != 0 else 0 for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            DP(i, j, m, n, dp)
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            DP(i, j, m, n, dp)
    
    return dp