def nextGreat(nums):
    if len(nums) == 0:
        return 
    stack = []
    stack.append(nums[0])

    for i in range(1, len(nums)):
        while len(stack) != 0 and nums[i] > stack[-1]:
            num = stack.pop()
            print(num, ': ', stack[i])
        stack.append(nums[i])

    while len(stack) != 0:
        print(stack.pop(), ': -1')


def nextGreat2(nums):
    stack, r = [], [-1] * len(nums)
    for i in range(len(nums)):
        while stack and nums[stack[-1]] < nums[i]:
            r[stack.pop()] = nums[i]
        stack.append(i)
        print(r)
    for i in range(len(nums)):
        while stack and nums[stack[-1]] < nums[i]:
            r[stack.pop()] = nums[i]
        if stack == []:
            break
    return r