# 验证数独游戏是否正确
def sudoku(matrix):
    n = len(matrix)
    result_row = result_col = result_blk = 0

    for i in range(n):
        result_row = result_col = result_blk = 0
        for j in range(n):
            # check row
            temp = matrix[i][j]
            if ((result_row & (1 << (temp - 1))) == 0):
                result_row = result_row | (1 << (temp - 1))
            else:
                print('row: ', i, j)
                return False
            
            # check column
            temp = matrix[j][i]
            if ((result_row & (1 << (temp - 1))) == 0):
                result_row = result_row | (1 << (temp - 1))
            else:
                print('row: ', j, i)
                return False
            
            # check block
            idx_row = (i // 3) * 3 + j // 3
            idx_col = (i % 3) * 3 + j % 3
            temp = matrix[idx_row][idx_col]
            if ((result_row & (1 << (temp - 1))) == 0):
                result_row = result_row | (1 << (temp - 1))
            else:
                print('block: ', idx_row, idx_col)
                return False
    return True
