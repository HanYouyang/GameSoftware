def minStep(height):
    return minStepHelper(height, 0, len(height), 0)
def minStepHelper(height, left, right, h):
    if left >= right:
        return 0
    m = left
    for i in range(left, right):
        if height[i] < height[m]:
            m = i
        
    return min(right - left, minStepHelper(height, left, m ,height[m]) +
                            minStepHelper(height, m + 1, right, height[m]) + height[m] - h)

