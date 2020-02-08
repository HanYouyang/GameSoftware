def uniquePaths(m, n):
    aux = [[1 for x in range(n)] for x in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            aux[i][j] = aux[i][j - 1] + aux[i - 1][j]
    return aux[-1][-1]

def uniquePaths2(m, n):
    aux = [ 1 for x in range(n)]
    for i in range(1, m):
        for j in range(1, n):
            aux[j] = aux[j] + aux[j - 1]
    return aux[-1]

def uniquePaths3(obstacleGrid):
    m, n = len(obstacleGrid), obstacleGrid[0]
    dp = [1] + [0] * (n - 1)
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[n - 1]