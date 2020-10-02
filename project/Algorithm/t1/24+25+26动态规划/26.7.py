def lcs(x, y, m, n):
    matrix = [[0 for k in range(n + 1)] for l in range(m + 1)]
    result = 0

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                matrix[i][j] = 0
            elif x[i - 1] == y[i - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
                result = max(result, matrix[i][j])
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])
    return result
