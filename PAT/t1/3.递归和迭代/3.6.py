def hanoi(n, start, end, by):
    if (n == 1):
        print('Move from' + start + ' to ' + end)
    else:
        hanoi(n - 1, start, by, end)
        hanoi(1, start, end, by)
        hanoi(n - 1, by, end, start)