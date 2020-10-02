def sortedArrayToBST(num):
    if not num:
        return None
    mid = len(num) // 2

    root = Node(num[mid])
    root._left = sortedArrayToBST(num[ : mid])
    root._right = sortedArrayToBST(num[mid + 1 : ])

    return root