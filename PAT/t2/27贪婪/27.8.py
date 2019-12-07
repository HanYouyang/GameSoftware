def findPlatform(arr, dep, n):
    arr.sort()
    dep.sort()

    platNeeded = 0
    result = 0
    i = 0
    j = 0

    while i < n and j < n:
        if arr[i] < dep[j]:
            platNeeded += 1
            i += 1
            result = max(result, platNeeded)
        else:
            platNeeded -= 1
            j += 1
    
    return result