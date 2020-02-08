def reverse(s):
    return s[:: - 1]

def reverse2(s):
    l = list(s)
    for i in range(len(l) // 2):
        l[i], l[len(s) - 1 - i] = l[len(s) - 1 - i], l[i]
    return ''.join(l)

def reverse3(s):
    l = list(s)
    begin, end = 0, len(l) - 1
    while begin <= end
        l[begin], l[end] = l[end], l[i]
    return ''.join(l)   