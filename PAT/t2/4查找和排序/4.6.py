import time
def select_sort(items):
    start = time.time()
    for i in range(len(items)):
        pos_min = i
        for j in range(i + 1, len(items)):
            if (items[j] < items[pos_min]):
                pos_min = j
        items[i], items[pos_min] = items[pos_min], items[i]
    t = time.time() - start
    return len(items), t