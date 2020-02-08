def miniumCost(x, y, m, n):
    res = 0
    x.sort(reverse = True)
    y.sort(reverse = True)
    
    hzntl = 1
    vert = 1
    i = 0
    j = 0
    while i < m and j < n:
        if x[i] > y[j]:
            res += x[i] * vert
            hzntl += 1
            i += 1
        else:
            res += y[j] * hzntl
            vert += 1
            j += 1
    
    total = 0
    while i < m:
        total += x[i]
        i += 1
    res += total * vert

    total = 0
    while j < n:
        total += y[j]
        j += 1
    res += total * hzntl

    return res