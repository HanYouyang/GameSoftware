class AdvBST5(AdvBST4):
    def printPostorderIter(self):
        node = self._root
        stack = []
        stack.append(node)

        while len(stack) != 0:
            node = stack[-1]
            if node._left is None and node._right is None:
                pop = stack.pop()
                print('[', node._item, ']', end = ' ')
            else:
                if node._right is not None:
                    stack.append(node._right)
                    node._right = None
                if node._left is not None:
                    stack.append(node._left)
                    node._left = None
        print('')

    def printPostorderIter2(self):
        stack = [(self._root, False)]
        while stack:
            node, visited = stack.pop()
            if node:
                if visited:
                    print('[', node._item, ']', end = ' ')
                else:
                    stack.append((node, True))
                    stack.append((node._right, False))
                    stack.append((node._left, False))
