def searche(alist):
    if len(alist) == 0:
        return - 1

    left, right = 0, len(alist) - 1
    while left + 1 < right:
        if alist[left] < alist[right]:# 此时就是sorted
            return alist[left]
        mid = left + (right - left) // 2
        if alist[mid] >= alist[left]:
            left = mid + 1
        else:
            right = mid
    
    if alist[left] < alist[right]:# 兜底是配合上面的程序用的
        return alist[left]
    else:
        return alist[right]

def searche2(alist, item):
    if len(alist) == 0:
        return - 1

    left, right = 0, len(alist) - 1
    while left + 1 < right:
        mid = left + (right - left) // 2
        if alist[mid] == item:
            right = mid
        
        if alist[left] < alist[mid]:
            if alist[left] <= item and item <= alist[mid]:
                right = mid
            else:
                left = mid
        else:
            if alist[left] <= item and item <= alist[right]:
                left = mid
            else:
                right = mid

    if alist[left] == item:
        return left
    if alist[right] == item:
        return right

def searche3(alist, item):
    if len(alist) == 0:
        return - 1

    left, right = 0, len(alist) - 1
    while left + 1 < right:
        mid = left + (right - left) // 2
        if alist[mid] == item:
            right = mid
        elif alist[mid] < item:
            left = mid
        elif alist[mid] > item:
            right = mid
    
    if alist[left] >= item:
        return left
    if alist[right] >= item:
        return right
    
    return right + 1