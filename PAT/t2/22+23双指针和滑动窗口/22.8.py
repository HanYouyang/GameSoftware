def majority2(alist):
    n1 = n2 = None
    c1 = c2 = 0
    for num in alist:
        if n1 == num:
            c1 += 1
        elif n2 == num:
            c2 += 1
        elif c1 == 0:
            n1, c1 = num, 1
        elif c2 == 0:
            n2, c2 = num, 1
        else:
            c1, c2 = c1 - 1, c2 - 1
    size = len(alist)
    return [n for n in (n1, n2)
                if n is not None and alist.count(n) > size / 3]