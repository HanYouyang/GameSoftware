def paciAtlan(matrix):
    if not matrix: return []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    m = len(matrix)
    n = len(matrix[0])
    p_visited = [[False for _ in range(n)] for _ in range(m)]
    a_visited = [[False for _ in range(n)] for _ in range(m)]
    result = []

    for i in range(m):
        dfs(matrix, i, 0, p_visited, m, n)
        dfs(matrix, i, n - 1, a_visited, m, n)
    for j in range(n):
        dfs(matrix, 0, j, p_visited, m, n)
        dfs(matrix, m - 1, j, a_visited, m, n)

    for i in range(m):
        for j in range(n):
            if p_visited[i][j] and a_visited[i][j]:
                result.append([i, j])
    return result
def dfs(matrix, i, j, visited, m, n):
    visited[i][j] = True
    for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x, y = i + dir[0], j + dir[1]
        if x < 0 or x >= m or y < 0 or y >= n or visited[x][y] or matrix[x][y] < matrix[i][j]:
            continue
        dfs(matrix, x, y, visited, m, n)


from collections import deque
def paciAtlan2(matrix):
    if not matrix: return []
    m, n = len(matrix), len(matrix[0])
    def bfs(reachable_ocean):
        q = deque(reachable_ocean)
        while q:
            (i, j) = q.popleft()
            for (di, dj) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if 0 <= di + i < m and 0 <= dj + j < n and (di + i, dj + j) not in reachable_ocean and matrix[di + i][dj + j] >= matrix[i][j]:
                    q.append((di + i, dj + j))
                    reachable_ocean.add((di + i, dj + j))
        return reachable_ocean
    pacfic = set([(i, 0) for i in range(m)] + [(0, j) for j in range(1, n)])
    atlantic = set([(i, n - 1) for i in range(m)] + [(m - 1, j) for j in range(n - 1)])
    return list(bfs(pacfic) & bfs(atlantic))