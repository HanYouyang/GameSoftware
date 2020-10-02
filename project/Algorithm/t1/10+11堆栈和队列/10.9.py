class queMakeStack:
    def __init__(self):
        self.queue = LinkedList()

    def push(self, x):
        self.queue.addLast(x)

    def pop(self):
        size = self.queue.size()
        for i in range(1, size):
            self.queue.addLast(self.queue.removeFirst())
        self.queue.removeFirst()

    def top(self):
        size = self.queue.size()
        for i in range(1, size):
            self.queue.addLast(self.queue.removeFirst())
        result = self.queue.removeFirst()
        self.queue.addLast(result)
        return result
    