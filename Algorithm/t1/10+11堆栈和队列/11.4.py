def simplifyPath(path):
    lst = []
    splits = path.split('/')

    for s in splits:
        if s == '':
            continue
        if s == '.':
            continue
        if s == '..':
            if len(lst) != 0:
                lst.pop()
        else:
            lst.append(s)
    
    result = []
    if len(lst) == 0:
        return '/'

    result = ['/' + i for i in lst]
    return ''.join(result)

