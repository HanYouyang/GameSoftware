def search_peak(alist):
    return peak_helper(alist, 0, len(alist) - 1)

def peak_helper(alist, start, end):
    if start == end:
        return start
    
    if (start + 1 == end):
        if alist[start] > alist[end]:
            return start
        return end
    
    mid = (start + end) // 2
    if alist[mid] > alist[mid - 1] and alist[mid] > alist[mid + 1]:
        return mid
    if alist[mid - 1] > alist[mid] and alist[mid] > alist[mid + 1]:
        return peak_helper(alist, start, mid - 1)
    return peak_helper(alist, mid + 1, end)