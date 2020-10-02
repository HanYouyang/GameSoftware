def fracKnapsack(capicity, weights, values):
    numItems = len(values)
    valuePerWeight = sorted([[v / w, w, v] for v, w in zip(values, weights)], reverse = True)
    print(valuePerWeight)
    totalCost = 0
    for tup in valuePerWeight:
        if capicity >= tup[1]:
            capicity -= tup[1]
            totalCost += tup[2]
        else:
            totalCost += capicity * tup[0]
            break
    return totalCost