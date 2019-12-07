import time
def insert_sort(items):
    start = time.time()
    for sort_inx in range(1, len(items)):
        unsort_inx = sort_inx
        while unsort_inx > 0 and items[unsort_inx - 1] > items[unsort_inx]:
            items[unsort_inx - 1], items[unsort_inx] = items[unsort_inx], items[unsort_inx - 1]
            unsort_inx = unsort_inx - 1
    t = time.time() - start
    return len(items), t