def merge(intervals):
    intervals.sort(key = lambda x: x.start)

    merged = []
    for interval in intervals:
        if not merged or merged[- 1].end < interval.start:
            merged.append(interval)
        else:
            merged[- 1].end = max(merged[- 1].end, interval.end)
    return merged

class Interval:
    def __int__(self, s = 0, e = 0):
        self.start = s
        self.end = e
    def __str__(self):
        return '[' + self.start + ',' + self.end + ']'
    def __repr__(self):
        return '[%s, %s]' % (self.start, self.end)