def merge(left, right):
    result = list()
    i, j = 0, 0
    inv_count = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        elif right[j] < left[i]:
            result.append(right[j])
            j += 1
            inv_count += (len(left) - i)
    result += left[i : ]
    result += right[j : ]
    return result, inv_count

def countInvFast(array):
    if len(array) < 2:
        return array, 0
    middle = len(array) // 2
    left, inv_left = countInvFast(array[ : middle])
    right, inv_right = countInvFast(array[middle : ])
    merged, count = merge(left, right)
    count += (inv_left + inv_right)
    return merged, count