from collections import Counter as ct
def topKFrequent(nums, k):
    return [k for (k, v) in ct(nums).most_common(k)]