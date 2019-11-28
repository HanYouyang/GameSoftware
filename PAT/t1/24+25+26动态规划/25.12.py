def movingBoard(board):
    result = board
    m = len(board)
    n = len(board[0])
    for i in range(1, m):
        for j in range(0, n):
            result[i][j] = max(0 if j == 0 else result[i - 1][j - 1], result[i - 1][j], 0 if j == n - 1 else result[i - 1][j + 1]) + board[i][j]
    return max(result[-1])

