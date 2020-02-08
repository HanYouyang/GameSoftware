class AdvBST3(AdvBST2):

    def zigzag(self):
        if not self._root:
            return []
        res, temp, stack, flag = [], [], [self._root], 1
        while stack:
            for i in range(len(stack)):
                node = stack.pop(0)
                temp += [node._item]
                if node._left:
                    stack += [node._left]
                if node._right:
                    stack += [node._right]
            res += [temp[::flag]]# 这里使用的是反序步骤的特性
            temp = []
            flag *= -1
        return res

