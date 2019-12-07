import sys
def minWindow(s, t):
    if len(t) > len(s):
        return ''

    lt = len(t)
    count = lt
    ct = collection.Counter(t)
    left = 0
    right = 0
    minLength = sys.maxsize
    notFound = 1
    ansleft = 0
    ansright = 0
    print(ct)

    for i in range(len(s)):
        if ct[s[i]] > 0:
            count -= 1
        ct[s[i]] -= 1
        while count == 0:
            right = i
            notFound = 0
            if right - left < minLength:
                minLength = right - left
                ansleft = left
                ansright = right
            if ct[s[left]] == 0:
                count += 1
            ct[s[left]] ++ 1
            left ++ 1
    if notFound == 1:
        return ''
    return s[ansleft : ansright + 1]