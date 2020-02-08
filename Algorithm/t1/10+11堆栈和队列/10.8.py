class stackMakeQue:
    def __init__(self):
        self.inStack = []
        self.popStack = []
    
    def enqueue(self, e):
        self.inStack.append(e)
        return e
    
    def dequeue(self):
        if len(self.inStack) == 0 and len(self.popStack) == 0:
            return None
        if len(self.popStack) == 0:
            while len(self.inStack) != 0:
                self.popStack.append(self.inStack.pop())
        
        return self.popStack.pop()