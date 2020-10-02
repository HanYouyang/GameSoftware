def removeDuplicate(alist):
    if not alist:
        return 0
    tail = 0
    for j in range(1, len(alist)):
        if alist[j] != alist[tail]:
            tail += 1
            alist[tail] = alist[j]
    return tail + 1

def removeDuplicate2(alist):
    i = 0
    for n in alist:
        if i == 0 or n > alist[i - 1]:
            alist[i] = n
            i += 1
    return i

