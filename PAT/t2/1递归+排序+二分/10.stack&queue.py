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
# 
# 
# 