ans = 0 
for i in range(n):
    for j in range(i, n):
        sum = 0
        for k in range(i, j):
            sum += a[k]
        if sum > ans:
            ans = sum
return ans

ans = 0
for i in range(n):
    sum = 0
    for j in range(i, n):
        sum += a[j]
        if sum > ans:
            ans = sum
return ans

def solve(nums):
    if n == 1:
        return max(a[1], 0)
    ans = max(slove(numsLeft), solve(numsRight))
    ansl = sum = 0
    for i in range(1, n // 2):
        sum = sum + a[i]
        if sum > ansl:
            ansl = sum
    ansr = sum = 0
    for i in range(n // 2 + 1, n):
        sum = sum + a[i]
        if sum > ansr:
            ansr = sum
    return max(ans, ansl + ansr)

ans = 0
b = 0 
for j in range(n):
    b = max(b + a[j], a[j])
    ans = max(b, ans)
return ans

