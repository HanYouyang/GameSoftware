def calPoints(ops):
    stack = []
    for op in ops:
        if op == '+':
            stack.append(stack[- 1] + stack[- 2])
        elif op == 'c':
            stack.pop()
        elif op == 'D':
            stack.append(2 * stack[- 1])
        else:
            stack.append(int(op))
    return sum(stack)
