from collections import deque
class AdvBST1(biSearchTree):
    def levelOrder(self):
        if not self._root:
            return []
        
        ret = []
        level = [self._root]

        while level:
            currentNodes = []
            nextLevel = []
            for node in level:
                currentNodes.append(node._item)
                if node._left:
                    nextLevel.append(node._left)
                if node._right:
                    nextLevel.append(node._right)
            ret.append(currentNodes)
            level = nextLevel
        
        return ret

class AdvBST2(biSearchTree):
    def levelOrder(self):
        if not self._root:
            return []
        
        ans = []
        level = [self._root]

        while level:
            ans.insert(0, [node._item for node in level])
            temp = []
            for node in level:
                temp.extend([node._left, node._right])
            level = [leaf for leaf in temp if leaf]

        return ans

    def levelOrder2(self):
        if not self._root:
            return []
        
        ans = []
        level = [self._root]

        while level:
            ans.append([node._item for node in level])# 就这里和最后相当于反过来
            temp = []
            for node in level:
                temp.extend([node._left, node._right])
            level = [leaf for leaf in temp if leaf]
        ans.reverse()
        return ans