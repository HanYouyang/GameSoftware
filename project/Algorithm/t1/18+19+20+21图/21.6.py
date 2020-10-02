def updateMatrix(matrix):
    q, m, n = [], len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if matrix[i][j] != 0:
                matrix[i][j] = 0x7fffffff
            else:
                q.append((i, j))
    for i, j in q:
        for r, c in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
            z = matrix[i][j] + 1
            if 0 <= r < m and 0 <= c < n and matrix[r][c] > z:
                matrix[r][c] = z
                q.append((r, c))
    return matrix