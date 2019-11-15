from collections import Counter
def wordCount(s):
    wordcount = Counter(s.split())
    print(wordcount)

def firstUniqChar(s):
    letters = 'sfdftewrfewfewfwetdsfsdfasfererewt'
    index = [s.index(i) for i in letters if s.count(i) == 1]
    return min(index) if len(index) > 0 else -1