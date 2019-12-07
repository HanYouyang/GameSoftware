def findSmallest(m, s):
    if s == 0:
        if m == 1:
            print('0')
        else:
            print('Impossible')
        return

    if s > 9 * m:
        print('Impossible')
        return
    
    res = [0 for i in range(m + 1)]
    s -= 1
    for i in range(m - 1, 0, -1):
        if s > 9:
            res[i] = 9
            s -= 9
        else:
            res[i] = s
            s = 0
    
    res[0] = s + 1
    print('Smallest number is ', end = '')
    for i in range(m):
        print(res[i], end = '')