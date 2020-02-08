# 01
# 1 用栈实现队列
# 用两个 去除头部就是搬空左边全部移动到右边
# 左边继续push元素 但pop在右边
# 注意既然实现队列实则复杂度还是队列的复杂度
class QueueWithTwoStacks:
    def __init__(self):
        self.insertStack = []
        self.popStack = []
    def enqueue(self, e):
        self.insertStack.append(e)
        return e
    def dequeue(self):
        if len(self.insertStack) == 0 and len(self.popStack) == 0:
            return None
        if len(self.popStack) == 0:
            while len(self.insertStack) != 0:
                self.popStack.append(self.insertStack.pop())
        return self.popStack.pop()

# 2 用队列实现栈
# 用单个队列 每次删除都是全放自己后面 
class StackWithQueue:
    def __init__(self):
        self.queue = LinkedList()
    # Push element x onto stack.
    def push(self, x):
        self.queue.add_last(x)
    # Removes the element on top of the stack.
    def pop(self):
        size = self.queue.size()
        for i in range(1, size):
            self.queue.add_last(self.queue.remove_first())
        self.queue.remove_first()
    def top(self):
        size = self.queue.size()
        for i in range(1, size):
            self.queue.add_last(self.queue.remove_first())
        result = self.queue.remove_first()
        self.queue.add_last(result)
        return result

# 3 最小栈
# 可以总能常数时间获得最小值
# 1.用两个栈 另外一个stack存最小值
# 2.栈里面存自己定义的class
import sys
from ArrayStack import ArrayStack
class MinStack(ArrayStack):
    def __init__(self):
        super(MinStack, self).__init__()
    def push(self, v):       
        newMin = min(v, self.min())
        super(MinStack, self).push(NodeWithMin(v, newMin))
    def min(self):
        if (super(MinStack, self).is_empty()):
            return sys.maxsize
        else:
            return super(MinStack, self).top()._min
class NodeWithMin:
    def __init__(self, v, min):
        self._value = v
        self._min = min
# 时间复杂度降低但是空间复杂度增加
class MinStack2(ArrayStack):
    def __init__(self):
        super(MinStack2, self).__init__()
        self.min_stack = ArrayStack()
    def push(self, value):
        if value <= self.min():
            self.min_stack.push(value)
        super(MinStack2, self).push(value)
        return value
    def min(self):
        if self.min_stack.is_empty():
            return sys.maxsize
        else:
            return self.min_stack.top()    
    def pop(self):
        value = super(MinStack2, self).pop()
        if value == self.min():
            self.min_stack.pop()
        return value

# 4.1 一个数组实现两个栈
# 一个从前往后一个从后往前
class twoStacks:
    def __init__(self, n): 
        self.size = n
        self.arr = [None] * n
        self.top1 = -1
        self.top2 = self.size
    # Method to push an element x to stack1
    def push1(self, x):
        # There is at least one empty space for new element
        if self.top1 < self.top2 - 1 :
            self.top1 = self.top1 + 1
            self.arr[self.top1] = x
        else:
            print("Stack Overflow ")
    # Method to push an element x to stack2
    def push2(self, x):
        # There is at least one empty space for new element
        if self.top1 < self.top2 - 1:
            self.top2 = self.top2 - 1
            self.arr[self.top2] = x
        else :
           print("Stack Overflow ")
    # Method to pop an element from first stack
    def pop1(self):
        if self.top1 >= 0:
            x = self.arr[self.top1]
            self.top1 = self.top1 -1
            return x
        else:
            print("Stack Underflow ")
    # Method to pop an element from second stack
    def pop2(self):
        if self.top2 < self.size:
            x = self.arr[self.top2]
            self.top2 = self.top2 + 1
            return x
        else:
            print("Stack Underflow ")
# 4.2 一个数组实现三个栈
# 1.分成三份
# 2.建立链表
# 3.dict存储空间

# 5 栈排序
# 有额外栈用来排序 有单个数字的额外空间
# 右边栈已排序可以放进去
def sortStack(s):
    r = ArrayStack()
    while not s.is_empty():
        tmp = s.pop()
        while not r.is_empty() and r.top() > tmp:
            s.push(r.pop())
        r.push(tmp)
    return r

# 02
from LinkedList import LinkedList
from LinkedList import Node
from ArrayStack import ArrayStack
# 1.1 反转字符串
# stack放进去再拿出来
def reverse(s):
    lst = []
    for i in s:
        lst.append(i)
    result = []
    while len(lst) != 0:
        result.append(lst.pop())
    return ''.join(result)

# 1.2 判断回文
# 正反相等即可
def isPalindrome(s):
    r = reverse(s)
    return r == s

# 2 合法括号
# 程序写的不严谨因为没有考虑多种括号的综合
def isValid(s):
    stack = []
    for c in s:
        if (c == '(' or c == '[' or c == '{'):
            stack.append(c)
        else:
            if len(stack)==0:
                return False
            if (   (c == ')' and stack[-1] == '(')
                or (c == ']' and stack[-1] == '[')
                or (c == '}' and stack[-1] == '{')):
                stack.pop()
            else:
                return False
    return len(stack) == 0

# 3 最简路径
# 面试给出步骤
# 一个点是当前不做 正常元素push 两个点是上层pop
def simplifyPath(path):
    lst = []
    splits = path.split("/")
    for s in splits:
        if s == "":
            continue
        if s == ".":
            continue
        if s == "..":
            if len(lst) != 0:
                lst.pop()
        else:
            lst.append(s)
    result = []
    if len(lst) == 0:
        return "/"
    result = ['/' + i for i in lst]
    return ''.join(result)

# 4 解密字符串
# 面试要说明1放什么 2什么时候push 3什么时候pop
# 找到右括号才能下结论拿到什么东西
# stack放tuple
# 找到左括号才能下结论到底数字是多少位
def decodeString(s):
    stack = []
    stack.append(["", 1])
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif ch == '[':
            stack.append(["", int(num)])
            num = ""
        elif ch == ']':
            st, k = stack.pop()
            stack[-1][0] += st * k
        else:
            stack[-1][0] += ch
    return stack[0][0]

# 5 篮球游戏
# 模拟规则
def calPoints(ops):
    stack = []
    for op in ops:
        if op == '+':
            stack.append(stack[-1] + stack[-2])
        elif op == 'C':
            stack.pop()
        elif op == 'D':
            stack.append(2 * stack[-1])
        else:
            stack.append(int(op))
    return sum(stack)

# 6 星球碰撞
# 模拟
def asteroidCollision(asteroids):
    ans = []
    for new in asteroids:
        while ans and new < 0 < ans[-1]:
            if ans[-1] < -new:
                ans.pop()
                continue
            elif ans[-1] == -new:
                ans.pop()
            break # 这个题还是不真明白
        else:
            ans.append(new)
    return ans

# 03
# 1.1 下个更大数字
# 找到数组中下个比当前值大的数字
# 给栈如果有大于当前的就pop得到当前最大值 往后继续记录
from ArrayStack import ArrayStack
def nextGreat(nums):
    if len(nums) == 0:
        return
    stack = []
    stack.append(nums[0])
    for i in range(1, len(nums)):
        while (len(stack) != 0 and nums[i] > stack[-1]):
            num = stack.pop()
            print(num, ": ", array[i])
        stack.append(nums[i])
    while len(stack) != 0:
        print(stack.pop(), ": -1")

# 1.2 下个最大数字2
# 循环数组 
# 运行两遍就是看数组后面的值 重新与前面数值比较
def nextGreat2(nums):
    stack, r = [], [-1] * len(nums)
    for i in range(len(nums)):
        while stack and (nums[stack[-1]] < nums[i]):
            r[stack.pop()] = nums[i]
        stack.append(i)
    print(r)
    for i in range(len(nums)):
        while stack and (nums[stack[-1]] < nums[i]):
            r[stack.pop()] = nums[i]
        if stack == []:
            break
    return r

# 1.3 每日气温
# 多少天后有更高温度
# stack里面放tuple 第一个是温度 第二个是index
def dailyTemperatures(temperatures):
    if not temperatures: return []
    result, stack = [0] * len(temperatures), []
    stack.append((temperatures[0], 0))
    for i in range(1, len(temperatures)):
        while stack:
            prev = stack[-1]
            if prev[0] < temperatures[i]:
                result[prev[1]] = i - prev[1]
                stack.pop()
            else:
                break
        stack.append((temperatures[i], i))
    return result
def dailyTemperatures2(temperatures):
    if not temperatures: return []
    result, stack = [0] * len(temperatures), []
    stack.append(0)
    for i in range(1, len(temperatures)):
        while stack:
            prev = stack[-1]
            if temperatures[prev] < temperatures[i]:
                result[prev] = i - prev
                stack.pop()
            else:
                break
        stack.append(i)
    return result

# 2 滑动窗口最大值
# 三个相连数字的最大值 此时放到数组里面