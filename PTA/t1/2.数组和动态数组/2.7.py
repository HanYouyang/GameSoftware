def magic_aquare(n):
    magic = [[0] * (n) for i in range(n)]
    row = n - 1
    col = n // 2
    magic[row][col] = 1
    for i in range(2, n * n + 1):
        try_row = (row + 1) % n
        try_col = (col + 1) % n

        if (magic[try_row][try_col] == 0):
            row = try_row
            col = try_col
        else:
            row = (row - 1 + n) % n # python数组允许负值，必须+n避免复数出现

        magic[row][col] = i

    for x in magic:
        print(x, sep = ' ')