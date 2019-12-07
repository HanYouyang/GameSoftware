import sys
def printCloses(ar1, ar2):
    m = len(ar1)
    n = len(ar2)

    diff = sys.maxsize

    p1 = 0
    p2 = 0

    while p1 < m and p2 < n:
        if abs(ar1[p1] - ar2[p2]) < diff:
            diff = abs(ar1[p1] - ar2[p2])
        if ar1[p1] > ar2[p2]:
            p2 += 1
        else:
            p1 += 1
            
    return diff