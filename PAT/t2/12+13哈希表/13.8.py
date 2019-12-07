def findWords(words):
    line1, line2, line3 = set('qwer'), set('asdf'), set('zxcv')
    ret = []
    for word in words:
        w = set(word.lower())
        if w.issubset(line1) or w.issubset(line2) or w.issubset(line3):
            ret.append(word)
    return ret