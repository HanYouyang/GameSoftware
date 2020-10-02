def findMaxAvg(nums, k):
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    movingSum = max(p[i + k] - p[i] for i in range(len(nums) - k + 1))
    return movingSum / float(k)

def findMaxAvg2(nums, k):
    movingSum = 0.0
    for i in range(k):
        movingSum += nums[i]
    res = movingSum
    for j in range(k, len(nums)):
        movingSum += nums[j] - nums[j - k]
        res = max(res, movingSum)
    return res / k