class AdvBST3(AdvBST2):
    def printInorderInter(self):
        node = self._root
        stack = []

        while True:
            while node is not None:
                stack.append(node)
                node = node._left
            
            if len(stack) == 0:
                return 
            
            node = stack.pop()
            print('[', node._item, ']', end = ' ')
            node = node._right

