# 哈希高级用法 滚动哈希（字符串查找） 缓存
# 注意dict set counter defaultDict区别
# 1.1 字符计数
# counter就是专门计数器只能用来整数
# dict不能排序也没counter的排序函数
def letterCount(s):
    freq = {}
    for piece in s:
        # only consider alphabetic characters within this piece
        word = ''.join(c for c in piece if c.isalpha())
        if word:
            freq[word] = 1 + freq.get(word, 0) #default 0

    max_word = ''
    max_count = 0
    for (w,c) in freq.items():    # (key, value) tuples represent (word, count)
        if c > max_count:
            max_word = w
            max_count = c
    print('The most frequent word is', max_word)
    print('Its number of occurrences is', max_count)    
from collections import Counter
def letterCount2(s):
    c = Counter(x for x in s if x != " ")
    for letter, count in c.most_common(4):
        print('%s: %7d' % (letter, count))

# 1.2 单词计数
# 单词也可以用split分类
def wordCount(s):
    wordcount = Counter(s.split())
    print(wordcount)

# 1.3 找第一个唯一字符
# 先找到所有数字开辟dict
# python可以用count 其实连续循环两次效果更好
def firstUniqChar(s):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    index = [s.index(l) for l in letters if s.count(l) == 1]
    return min(index) if len(index) > 0 else -1

# 2.1 数组交集
# 未排序 排序的用数组里面有双指针
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))

# 2.2 数组交集2
# 未排序 结果要求重复元素出现
# 后面list元素放给dict可以查找
def intersect(nums1, nums2):
    dict1 = dict()
    for i in nums1:
        if i not in dict1:
            dict1[i] = 1
        else:
            dict1[i] += 1
    ret = []
    for i in nums2:
        if i in dict1 and dict1[i]>0:
            ret.append(i)
            dict1[i] -= 1
    return ret

# 3 石中找珠宝
# j为set 用s查
def numJewelsInStones(J, S):
    setJ = set(J)
    return sum(s in setJ for s in S)

# 4.1 包含重复
def containsDuplicate(nums):
    return len(nums) > len(set(nums))

# 4.2 包含重复2
# 索引不超过k的间距出现重复 排序后就是次数
def containsNearbyDuplicate(nums, k):
    dic = {}
    for i, v in enumerate(nums):
        if v in dic and i - dic[v] <= k:
            return True
        dic[v] = i
    return False

# 5 子域名访问计数
# 字符串灵活使用split
import collections 
def subdomainVisits(cpdomains):
    ans = collections.Counter()
    for domain in cpdomains:
        count, domain = domain.split()
        count = int(count)
        frags = domain.split('.')
        for i in range(len(frags)):
            ans[".".join(frags[i:])] += count

    return ["{} {}".format(ct, dom) for dom, ct in ans.items()]

# 6 键盘行
# 维持单个变量放回结果去
def findWords(words):
    line1, line2, line3 = set('qwertyuiop'), set('asdfghjkl'), set('zxcvbnm')
    ret = []
    for word in words:
        w = set(word.lower())# 检验一整个字符串
        if w.issubset(line1) or w.issubset(line2) or w.issubset(line3):
            ret.append(word)
    return ret

# 02
# 0.1 找共点最多线
# 1.暴力遍历所有线 再遍历点计数
# 2.dict存k和b的counter ton^2

# 0.2 LRU 最近访问网站
# 记录最近访问 三个备选 查放更新删除
# 如果用queue重复访问会消除错误 实则应使用双向链表+dict
# 在dict里面进行链接移动
# java有LinkedHashMap横向解决碰撞纵向是联系

# 1 单词模式
# 找abab等模式是否匹配单词的各种模式
# zip可以组成pair 先看set后的s和t一样长度 再看s和t长度相等？
def wordPattern(pattern, str):
    s = pattern
    t = str.split()
    return len(set(zip(s, t))) == len(set(s)) == len(set(t)) and len(s) == len(t)

# 2
# 
# 