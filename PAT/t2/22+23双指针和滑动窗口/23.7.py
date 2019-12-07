def strStr(haystack, needle):
    if len(haystack) < len(needle):
        return None
    i = 0
    while i < len(haystack) - len(needle) + 1:
        j = 0
        k = i
        while j < len(needle):
            if haystack[k] == needle[j]:
                j += 1
                k += 1
            else:
                break
        if j == len(needle):
            break
        else:
            i += 1
    if i == len(haystack) - len(needle) + 1:
        return None
    else:
        return haystack[i : ]

def strStr2(haystack, needle):
    if len(haystack) < len(needle):
        return None
    l1 = len(haystack)
    l2 = len(needle)
    for i in range(l1 - l2 + 1):
        count = 0
        while count < l2 and haystack[i + count] == needle[count]:
            count += 1
        if count == l2:
            return i
    return -1