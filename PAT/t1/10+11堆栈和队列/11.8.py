def asterCollision(aster):
    ans = []
    for new in aster:
        while ans and new < 0 < ans[-1]:# while要求比较之前的每一个数字
            if ans[-1] < -new:
                ans.pop()
                continue
            elif ans[-1] == -new:
                ans.pop()
                break
            else:
                ans.append(new)
    return ans