def printMaxActivities(acts):
    n = len(acts)
    sortActs = sorted(acts, key = lambda tup : tup[1])
    prev = sortActs[0]
    print(prev)
    for curr in sortActs:
        if curr[0] >= prev[1]:
            print(curr)
            prev = curr