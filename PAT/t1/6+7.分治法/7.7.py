def shuffleArray(a, left, right):
    if (right - left == 1):
        return 
    mid = (left + right) // 2
    temp = mid + 1
    mmid = (left + mid) // 2
    for i in range(mmid + 1, mid + 1):
        a[i], a[temp] = a[temp], a[i]
        temp += 1
    
    shuffleArray(a, left, mid)
    shuffleArray(a, mid + 1, right)

