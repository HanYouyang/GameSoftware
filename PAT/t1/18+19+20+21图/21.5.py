def longestIncreasingPath(matrix):
    if not matrix: return 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    m = len(matrix)
    n = len(matrix[0])
    cache = [[-1 for _ in range(n)] for _ in range(m)]
    res = 0
    for i in range(m):
        for j in range(n):
            cur_len = dfs(i, j, matrix, cache, m, n)
            res = max(res, cur_len)
    return res
def dfs(i, j, matrix, cache, m, n):
    if cache[i][j] != -1:
        return cache[i][j]
    res = 1
    for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x, y = i + direction[0], j + direction[1]
        if x < 0 or x >= m or y < 0 or y >= n or matrix[x][y] <= matrix[i][j]:
            continue
        length = 1 + dfs(x, y, matrix, cache, m, n)
        res = max(length, res)
    cache[i][j] = res
    return res