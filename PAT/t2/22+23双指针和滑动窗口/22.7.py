def majority(alist):
    result = count = 0
    for i in alist:
        if count == 0:
            result = i
            count = 1
        elif result == i:
            count += 1
        else:
            count -= 1
    return result

