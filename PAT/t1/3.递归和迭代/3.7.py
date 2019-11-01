def moves(n):
    if n == 0:
        return
    moves(n - 1)
    print(n) # 自动换行了
    moves(n - 1)

def moves_ins(n, forward):
    if n == 0:
        return
    moves_ins(n - 1, True)
    print('enter ', n) if forward else print('exit ', n)
    moves_ins(n - 1, False)