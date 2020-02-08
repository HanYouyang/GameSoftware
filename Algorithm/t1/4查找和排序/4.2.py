def bi_search_iter(alist, item):
    left, right = 0, len(alist) - 1
    while left <= right:# 满足这个条件才运行下面程序
        mid = left + (right - left) // 2
        if alist[mid] < item:
            left = mid + 1
        elif alist[mid] > item:
            right = mid - 1
        else:
            return mid
    return - 1

def bi_search_re(num_list, val):
    return bi_search(0, len(num_list), val)
def bi_search(l, h, val):
    if l > h:
        return - 1
    mid = l + (h - l) // 2
    if (h[mid] == val):
        return mid
    elif (h[mid] < val):
        return bi_search(mid + 1, h, val)
    else:
        return bi_search(l, mid + 1, val)

import unittest
class TestBinarySearch(unittest.TestCase):
    def setUp(self):
        self._f = bi_search_iter

    def test_empty(self):
        alist = []
        r = self._f(alist, 5)
        self.assertEqual(- 1, r)
if __name__ == '__main__':# 只能这么写不然不能通过
    unittest.main(argv = ['first-arg-is-ignored'], exit = False)