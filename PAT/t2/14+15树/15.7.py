class AdvBst1(biSearchTree):
    def getInter(self, key):
        node = self._root
        while node is not None:
            if key == node._item:
                return node._item
            if key < node._item:
                node = node.left
            else:
                node = node.right
        return None

class AdvBst2(AdvBst1):
    def addInter(self, value):
        newNode = Node(value)
        if self._root is None:
            self._root = newNode
            return
        
        current = self._root
        parent = None

        while True:
            parent = current
            if value == current._item:
                return
            if value < current._item:
                current = current.left
                if current is None:
                    parent._left = newNode
                    return 
            else:
                current = current._right
                if current is None:
                    parent._right = newNode
                    return
                    