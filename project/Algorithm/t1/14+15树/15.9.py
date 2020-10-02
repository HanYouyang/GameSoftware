class AdvBST4(AdvBST3):
    def printPreorderInter(self):
        ret = []
        stack = [self._root]

        while stack:
            node = stack.pop()
            if node:
                ret.append(node._item)
                stack.append(node._right)
                stack.append(node._left)
        return ret