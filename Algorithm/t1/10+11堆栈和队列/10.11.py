import sys
from ArrayStack import ArrayStack

class MinStack(ArrayStack):
    def __init__(self):
        super(MinStack, self).__init__()

    def push(self, v):
        newMin = min(v, self.min())
        super(MinStack, self).push(NodeWithMin(v, newMin))

    def min(self):
        if super(MinStack, self).is_empty():
            return sys.maxsize
        else:
            return super(MinStack, self).top()._min

class NodeWithMin:
    def __init__(self, v, min):
        self.value = v
        self._min = min

class MinStack2(ArrayStack):
    def __init__(self):
        super(MinStack2, self).__init__()
        self.minStack = ArrayStack()
    
    def push(self, value):
        if value <= self.min():
            self.minStack.push(value)
        super(MinStack2, self).push(value)
        return value
    
    def min(self):
        if self.minStack.isEmpty():
            return sys.maxsize
        else:
            return self.minStack.top()
    
    def pop(self):
        value = super(MinStack2, self).pop()
        if value == self.min():
            self.minStack.pop()
        return value