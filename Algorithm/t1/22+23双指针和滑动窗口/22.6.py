from itertools import accumulate
def maxSubarray(numbers, ceiling):
    cumSum = [0]
    cumSum = cumSum + numbers
    cumSum = list(accumulate(cumSum))

    l = 0
    r = 1
    maximum = 0
    while l < len(cumSum):
        while r < len(cumSum) and cumSum[r] - cumSum[l] <= ceiling:
            r += 1
        if cumSum[r - 1] - cumSum[l] > maximum:
            maximum = cumSum[r - 1] - cumSum[l]
            pos = (l, r - 2)
        l += 1
    return pos