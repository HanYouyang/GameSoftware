def maxAreaIsland(grid):
    m, n = len(grid), len(grid[0])

    def dfs(i, j):
        if 0 <= i < m and 0 <= j < n and grid[i][j]:
            grid[i][j] = 0
            return 1 + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i + 1, j) + dfs(i, j - 1)
        return 0
    
    result = 0
    for x in range(m):
        for y in range(n):
            if grid[x][y]:
                result = max(result, dfs(x, y))
    return result