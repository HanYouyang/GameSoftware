def rotate(matrix):
    n = len(matrix)
    result = [[0] * (n) for i in range(n)]

    for i in range(n):
        for j in range(n):
            result[j][n - 1 - i] = matrix[i][j]
    for x in result:
        print(x, sep = ' ')


def rotate_in_place(matrix):
    n = len(matrix)
    for layer in range(n // 2):
        first = layer
        last = n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = matrix[first][i]
            # left -> top
            matrix[first][i] = matrix[last - offset][first]
            # bottem -> left
            matrix[last - offset][first] = matrix[last][last - offset]
            # right -> bottem
            matrix[last][last - first] = matrix[i][last]
            # top -> right
            matrix[i][first] = top

    for x in matrix:
        print(x, sep = ' ')        
        