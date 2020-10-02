def dfs2(matrix, start, dest):
    visited, = [[False] * len(matrix[0]) for i in range(len(matrix))]
    return dfsHelper2(matrix, start, dest, visited)

def dfsHelper2(matrix, start, dest, visited):
    if matrix[start[0]][start[1]] == 1:
        return False
    if visited[start[0]][start[1]]:
        return False
    if start[0] == dest[0] and start[1] == dest[1]:
        return True
    
    visited[start[0]][start[1]] = True

    r = start[1] + 1
    l = start[1] - 1
    u = start[0] - 1
    d = start[0] + 1

    while r < len(matrix[0]) and matrix[start[0]][r] == 0:
        r += 1
    x = (start[0], r - 1)
    if dfsHelper2(matrix, x, dest, visited):
        return True
    
    while l >= 0 and matrix[start[0]][l] == 0:
        l -= 1
    x = (start[0], l + 1)
    if dfsHelper2(matrix, x, dest, visited):
        return True

    while u >= 0 and matrix[u][start[1]] == 0:
        u -= 1
    x = (u + 1, start[1])
    if dfsHelper2(matrix, x, dest, visited):
        return True
    
    while d >= 0 and matrix[d][start[1]] == 0:
        d += 1
    x = (u - 1, start[1])
    if dfsHelper2(matrix, x, dest, visited):
        return True

    return False