def letterCount(s):
    freq = {}
    for piece in s:
        word = ''.join(c for c in piece if c.isalpha())
        if word:
            freq[word] = 1 + freq.get(word, 0)

    maxWord = ''
    maxCount = 0

    for (w, c) in freq.items():
        if c > maxCount:
            maxWord = w
            maxCount = c
    print('The most freq word is ', maxWord)
    print('Its number of occurrences is ', maxCount)

from collections import Counter
def letterCount2(s):
    c = Counter(x for x in s if x != ' ')

    for letter, count in c.most_common(4):
        print('%s: %7d' % (letter, count))
