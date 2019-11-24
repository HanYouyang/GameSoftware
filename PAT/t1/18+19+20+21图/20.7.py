def floodFill(image, sr, sc, newcolor):
    rows, cols, orig_color = len(image), len(image[0]), image[sr][sc]
    if orig_color != newcolor:
        traverse(sr, sc)
    return image

def traverse(row, col):
    if (not (0 <= row < rows and 0 <= col < cols)) or image[row][col] != orig_color:
        return
    image[row][col] = newcolor
    [traverse(row + x, col + y) for (x, y) in ((0, 1), (1, 0), (0, -1), (-1, 0))] 