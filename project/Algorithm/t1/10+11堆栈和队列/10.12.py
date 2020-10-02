def sortStack(s):
    r = ArrayStack()

    while not s.isEmpty():
        tmp = s.pop()

        while not r.isEmpty() and r.top() > tmp:
            s.push(r.pop())
        r.push(tmp)
    
    return r