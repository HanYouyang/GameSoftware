from collections import deque
def ladderLength(beginWord, endWord, wordList):
    wordSet = set(wordList)
    wordSet.add(endWord)
    queue = deque([[beginWord, 1]])
    while queue:
        word, length = queue.popleft()
        if word == endWord:
            return length
        for i in range(len(word)):
            for c in 'abcdefg':
                nextWord = word[: i] + c + word[i + 1: ]
                if nextWord in wordSet:
                    wordSet.remove(nextWord)
                    queue.append([nextWord, length + 1])
    return 0