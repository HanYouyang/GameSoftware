# 01
# 1.1 树的大小
class AdvBST1(BinarySearchTree):
    def size(self):
        return self._size(self._root)
    def _size(self, node):
        if (not node):
            return 0
        return self._size(node._left) + self._size(node._right) + 1

# 1.2 最大深度 
# 判断树平衡 左右高度差不大于1
class AdvBST2(AdvBST1):    
    def maxDepth(self):
        return self._maxDepth(self._root)
    def _maxDepth(self, node):
        if (not node):
            return 0
        left_depth = self._maxDepth(node._left)
        right_depth = self._maxDepth(node._right)
        return max(left_depth, right_depth) + 1

# 1.3 判断平衡
# 让每个节点都平衡
class AdvBST3(AdvBST2):    
    def minDepth(self):
        return self._minDepth(self._root)
    def _minDepth(self, node):
        if (not node):
            return 0
        left_depth = self._minDepth(node._left)
        right_depth = self._minDepth(node._right)
        return min(left_depth, right_depth) + 1
    def isBalanced(self):
        return (self.maxDepth() - self.minDepth()) <= 1

# 1.4 找下限
# 遍历并且给出值的下限
class AdvBST4(AdvBST3):    
    def floor(self, key):
        return self._floor(self._root, key)
    def _floor(self, node, key):
        if (not node):
            return None
        if (key == node._item):
            return node
        if (key < node._item):
            return self._floor(node._left, key)
        t = self._floor(node._right, key)
        if t:
            return t
        return node# 递归给出的最后返回不是存起来是最终返回

# 1.5 判断BST
# 要用root给左右所有节点判断
import sys
class AdvBST5(AdvBST4):    
    def isBST(self):
        return self._isBST(self._root, -sys.maxsize, sys.maxsize)
    def _isBST(self, node, minval, maxval):
        if not node:
            return True
        if (node._item < minval or node._item > maxval):
            return False
        return self._isBST(node._left, minval, node._item) and self._isBST(node._right, node._item, maxval)

# 1.6  
# 
# 
# 
# 





