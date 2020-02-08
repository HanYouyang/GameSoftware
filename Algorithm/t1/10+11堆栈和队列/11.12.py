def daliyTemp2(tempList):
    if not tempList:
        return []
    result, stack = [0] * len(tempList), []
    stack.append(0)

    for i in range(1, len(tempList)):
        while stack:
            prev = stack[-1]
            if tempList[prev] < tempList[i]:
                result[prev] = i - prev
                stack.pop()
            else:
                break
        stack.append(i)
    return result