from bisect import bisect

def lengthOfLIS(nums):
    temp = []
    for num in nums:
        pos =  bisect(temp, num)
        if pos >= len(temp):
            temp.append(num)
        else:
            temp[pos] = num
    return len(temp)