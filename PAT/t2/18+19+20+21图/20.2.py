def dfs(matrix, start, dest):
    visited, = [[False] * len(matrix[0]) for i in range(len(matrix))]
    return dfsHelper(matrix, start, dest, visited)

def dfsHelper(matrix, start, dest, visited):
    if matrix[start[0]][start[1]] == 1:
        return False
    if visited[start[0]][start[1]]:
        return False
    if start[0] == dest[0] and start[1] == dest[1]:
        return True
    
    visited[start[0]][start[1]] = True

    if start[1] < len(matrix[0]) - 1:
        r = (start[0], start[1] + 1)
        if dfsHelper(matrix, r, dest, visited):
            return True
    if start[0] < len(matrix[0]) - 1:
        d = (start[0] + 1, start[1])
        if dfsHelper(matrix, d, dest, visited):
            return True
    if start[1] > 0:
        l = (start[0], start[1] - 1)
        if dfsHelper(matrix, l, dest, visited):
            return True
    if start[0] > 0:
        u = (start[0] - 1, start[1])
        if dfsHelper(matrix, u, dest, visited):
            return True   
    
    return False


def dfsIter(matrix, start, dest):
    visited, = [[False] * len(matrix[0]) for i in range(len(matrix))]
    stack = []
    stack.append(start)
    visited[start[0]][start[1]] = True

    idxs = [[0, 1], [0, -1], [-1, 0], [1, 0]]

    while len(stack) != 0:
        curr = stack.pop()
        if curr[0] == dest[0] and curr[1] == dest[1]:
            return True
        
        for idx in idxs:
            x = curr[0] + idx[0]
            y = curr[1] + idx[1]

            if x < 0 or x >= len(matrix) or y < 0 or y >= len(matrix[0]):
                continue
            if matrix[x][y] == 1:
                continue
            if visited[x][y] == True:
                continue
            visited[x][y] = True
            stack.append((x, y))

    return False