class AdvBST1(biSearchTree):
    def hasPathSum(self, s):
        return self.hasPathSumHelper(self._root, s)

    def hasPathSumHelper(self, node, s):
        if not node:
            return False
        if not node._left and node._right and node._item == s:
            return True
        s -= node._item

        return self.hasPathSumHelper(node._left, s) or self.hasPathSumHelper(node._right, s)

class AdvBST3(AdvBST2):
    def hasPathSum2Helper(self, node, s):
        if not node:
            return []
        res = []
        self.dfs(node, s, [], res)
        return res
    def dfs(self, node, s, ls, res):
        if not node._left and not node._right and s == node._item:
            ls.append(node._item)
            res.append(ls)
        if node._left:
            self.dfs(node._left, s - node._item, ls + [node._item], res)
        if node._right:
            self.dfs(node._right, s - node._item, ls + [node._item], res)

class AdvBST4(AdvBST3):
    def pathSum(self, target):
        return self.hasPathSumHelper(self._root, target)
    
    def findPath(self, node, target):
        if node:
            return int(node._item == target) +  \
                self.findPath(node._left, target - node._item) + \
                self.findPath(node._right, target - node._item)
        return 0
    
    def pathSumHelper(self, node, target):
        if node:
            return self.findPath(node, target) + \
                self.pathSumHelper(node._left, target) + \
                self.pathSumHelper(node._right, target)
        return 0