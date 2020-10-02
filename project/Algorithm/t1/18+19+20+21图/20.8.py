def findCircle(M):
    circle = 0
    n = len(M)

    for i in range(n):
        if M[i][i] != 1:
            continue
        friends = [i]
        while friends:
            f = friends.pop()
            if M[f][f] == 0:
                continue
            M[f][f] = 0
            for j in range(n):
                if M[f][j] == 1 and M[j][j] == 1:
                    friends.append(j)
        circle += 1
    return circle