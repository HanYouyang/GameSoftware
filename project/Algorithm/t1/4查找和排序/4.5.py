import time
def _bubble_sort(nums: list, reverse = False):
    start = time.time()
    for i in range(len(nums)):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    if reverse:
        nums.reverse()
    t = time.time() - start
    return len(nums), t

def bubble_sorted(nums: list, reverse = False):#  -> list
    nums_copy = list(nums)
    _bubble_sort(nums_copy, reverse = reverse)
    return nums_copy

def _bubble_sort(array):
    start = time.time()
    for i in range(len(array)):
        is_sorted = True
        for j in range(1, len(array) - i):
            if array[j] < array[j - 1]:
                array[j], array[j - 1] = array[j + 1], array[j]
                is_sorted = False
        if is_sorted: break
    t = time.time() - start
    return len(array), t

