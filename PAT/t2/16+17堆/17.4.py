def uglyNumber(num):
    for p in 2, 3, 5:
        while num % p == 0 < num:
            num /= p
    return num == 1

def nthUglyNumber(n):
    q2, q3, q5 = [2], [3], [5]
    ugly = 1
    for u in heapq.merge(q2, q3, q5):
        if n == 1:
            return ugly
        if u > ugly:
            ugly = u
            n -= 1
            q2 += 2 * u
            q3 += 3 * u
            q5 += 5 * u