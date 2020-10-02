def numJewInStone(j, s):
    count = 0
    for c in s:
        if c in j:
            count += 1
    return count

def numJewInStone2(j, s):
    setJ = set(j)
    return sum(sign in setJ for sign in s)