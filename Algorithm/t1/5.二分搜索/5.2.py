def binary_searche(alist, item):
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
    
    if alist[left] == item:
        return left
    if alist[right] == item:
        return right
    
    return - 1