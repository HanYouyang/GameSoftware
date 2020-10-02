class AdvBST5(AdvBST4):
    def lowestCommonAncestor(self, p, q):
        return lowestCommonAncestorHelper(self._root, p, q)

    def lowestCommonAncestorHelper(self, node, p, q):
        while node:
            if node._item > p._item and node._item > q._item:
                node = node._left
            if node._item < p._item and node._item < q._item:
                node = node._right
            else:
                return node