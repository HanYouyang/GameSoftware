def ruler_bad(n):
    assert(n >= 0)
    if (n == 1):
        return '1'
    return ruler_bad(n - 1) + ' ' + str(n) + ' ' + ruler_bad(n - 1)

def ruler(n):
    assert(n >= 0)
    if (n == 1):
        return '1'
    t = ruler(n - 1)
    return t + ' ' + str(n) + ' ' + t

def ruler2(n):
    result = ' '
    for i in range(1, n + 1):
        result = result + str(i) + ' ' + result
    return result

def draw_line(tick_length, tick_label = ' '):
    line = '-' * tick_length
    if tick_label:
        line += ' ' + tick_label
    print(line)

def draw_interval(center_length):
    if center_length > 0:
        draw_interval(center_length - 1)
        draw_line(center_length)
        draw_interval(center_length - 1)

def draw_rule(num_inches, major_length):
    draw_line(major_length, '0')
    for j in range(1, 1 + num_inches):
        draw_interval(major_length - 1)
        draw_line(major_length, str(j))