# 模拟 矩阵0判断
def zero(matrix):
    m = [None] * len(matrix)
    n = [None] * len(matrix[0])

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] == 0):
                m[i] = 1
                n[j] = 1

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (m[i] = 1 or n[j] = 1):
                matrix[i][j] = 0