def fib1(n):
    assert(n >= 0)# 值有效性检测
    if (n <= 2):
        return 1
    return fib1(n - 1) + fib1(n - 2)

def fib2(n):
    assert(n >= 0)
    a, b = 0, 1
    for i in range(1, n + 1):
        a, b = b, a + b
    return a

def fib3(n):
    assert(n >= 0)
    if (n <= 1):
        return (n, 0)
    (a, b) = fib3(n - 1)
    return (a + b, a)

def fib4(n):
    assert(n >= 0)
    result = [0, 1]
    for i in range(2, n + 1):
        result.append(result[ - 2] + result[ - 1])
    return result
        