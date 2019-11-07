def fast_power_flaw(x,n):
    if n <= 0:
        return 1
    elif n == 1:
        return x
    elif n % 2:# 间接获得值和判断，写法简洁
        return fast_power_flaw(x * x, n // 2) * x
    else:
        return fast_power_flaw(x * x, n // 2)

def fast_power(x, n):
    if n == 0:
        return 1.0
    elif n < 0:
        return 1 / fast_power(x, - n)
    elif n % 2:
        return fast_power_flaw(x * x, n // 2) * x
    else:
        return fast_power_flaw(x * x, n // 2)

