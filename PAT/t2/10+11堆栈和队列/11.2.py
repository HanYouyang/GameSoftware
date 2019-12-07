def reverse(s):
    lst = []
    for i in s:
        lst.append(i)
    result = []
    while len(lst) != 0:
        result.append(lst.pop())
    return ''.join(result)

def isPalindrome(s):
    r = reverse(s)
    return r == s

def isValid(s):
    stack = []
    for c in s:
        if c == '(' or c == '[' or c == '{':
            stack.append(c)
        else:
            if len(stack) == 0:
                return False
            if (c == ')' and stack[- 1] == '(')
                or (c == ']' and stack[- 1] == '[') 
                or (c == '}' and stack[- 1] == '{'):
                stack.pop()
            else:
                return False

    return len(stack) == 0   