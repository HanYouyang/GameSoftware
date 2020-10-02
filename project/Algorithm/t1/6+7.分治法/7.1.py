import functools
def prod(x, y):
    return str(eval('%s * %s' % (x, y)))
def plus(x, y):
    return str(eval('%s + %s' % (x, y)))
def one_to_n_product(d, x):
    print(d, x)
    result = ''
    carry = '0'
    for i, digit in enumerate(reversed(x)):
        r = plus(prod(d, digit), carry)
        if (len(r) == 1):
            carry = '0'
        else:
            carry = r[ : - 1]
        digit = r[- 1]
        result = digit + result
    return carry + result
def sum_middle_products(middle_products):
    max_length = max([len(md) for md in middle_products])
    for i, md in enumerate(middle_products):
        middle_products[i] = '0' * (max_length - len(md)) + md

    print(middle_products)
    carry = '0'
    result = ''
    for i in range(1, max_length + 1):
        row = [carry] + [md[ - i] for md in middle_products]
        r = functools.reduce(plus, row)
        carry, digit = r[ : - 1], r[ - 1]
        result = digit +result
    return carry + result
def algorithm(x, y):
    x, y = str(x), str(y)
    middle_products = []
    for i, digit in enumerate(reversed(y)):
        middle_products.append(one_to_n_product(digit, x) + '0' * i)
    print(middle_products)
    return int(sum_middle_products(middle_products))
