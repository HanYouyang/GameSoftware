from collections import defaultdict
import string
def findLadder(start, end, wordList):
    dic = set(wordList)
    dic.add(end)
    level = {start}
    parents = defaultdict(set)
    while level and end not in parents:
        nextLevel = defaultdict(set)
        for node in level:
            for char in string.ascii_lowercase:
                for i in range(len(start)):
                    n = node[: i] + char + node[i + 1: ]
                    if n in dic and n not in parents:
                        nextLevel[n].add(node)
        level = nextLevel
        parents.update(nextLevel)
    res = [[end]]
    print(parents)
    while res and res[0][0] != start:
        res = [[p] + r for in res for p in parents[r[0]]]
    return res