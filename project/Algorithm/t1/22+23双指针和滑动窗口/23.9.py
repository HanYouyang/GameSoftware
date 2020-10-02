def lengthOfLongestSubstring(s):
    usedchar = set()
    maxLength = 0
    i = j = 0
    n = len(s)
    while i < n and j < n:
        if s[j] not in usedchar:
            usedchar.add(s[j])
            j += 1
            maxLength = max(maxLength, j - i)
        else:
            usedchar.remove(s[i])
            i += 1
    return maxLength

def lengthOfLongestSubstring2(s):
    start = maxLength = 0
    usedChar = {}

    for i, c in enumerate(s):
        if c in usedChar and start <= usedChar[c]:
            start = usedChar[c] + 1
        else:
            maxLength = max(maxLength, i - start + 1)
        
        usedChar[c] = i
    return maxLength