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
# 要用root给左右所有节点判断 每一个传递都有最值或者极值
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

# 1.6 镜像树
# 类似归并算法 先递归左边 再递归右边
# 此处先反转左边 再反转右边
# 一层层从底层开始
class AdvBST6(AdvBST5):    
    def mirror(self):
        self._mirror(self._root)
    
    def _mirror(self, node):
        if (node is not None):
            self._mirror(node._left)
            self._mirror(node._right)
            
            temp = node._left
            node._left = node._right
            node._right = temp
            


# 1.7 相同树
# 
class AdvBST7(AdvBST6):    
    def sameTree(self, another):
        return self._sameTree(self._root, another._root)
    
    def _sameTree(self, nodeA, nodeB):
        if (nodeA is None and nodeB is None):
            return True
        if (nodeA is not None and nodeB is not None):
            return nodeA._item == nodeB._item and self._sameTree(nodeA._left, nodeB._left) and self._sameTree(nodeA._right, nodeB._right)
        return False

# 1.8 



# 2.1 Iterative Get
#
class AdvBST1(BinarySearchTree):
    def getIterative(self, key):
        node = self._root
        while (node is not None):
            if key == node._item:
                return node._item
            if key < node._item:
                node = node._left
            else:
                node = node._right
        return None



# 2.2 Iterative Add
class AdvBST2(AdvBST1):
    def addIterative(self, value):
        newNode = Node(value)
        if (self._root is None):
            self._root = newNode
            return
        
        current = self._root
        parent = None
        while True:
            parent = current
            if (value == current._item):
                return
            if (value < current._item):
                current = current._left
                if (current is None):
                    parent._left = newNode
                    return
            else:
                current = current._right
                if (current is None):
                    parent._right = newNode
                    return


# 2.3 Iterative Inorder Traversal
# Traversal Methods  
def print_inorder(self):
    self._print_inorder(self._root)
    print('')
def _print_inorder(self, node):
    if (node is None):
        return
    self._print_inorder(node._left)
    print ('[', node._item, ']', end = " ")
    self._print_inorder(node._right)

class AdvBST3(AdvBST2):
    def printInorderIterative(self):
        node = self._root
        stack = []
        
        while True:
            while (node is not None):
                stack.append(node)
                node = node._left
            if len(stack) == 0:
                return
            
            node = stack.pop()
            print ('[', node._item, ']', end = " ")
            node = node._right


# 2.4 Iterative Preorder Traversal
def print_preorder(self):
    self._print_preorder(self._root)
    print('')
def _print_preorder(self, node):
    if (node is None):
        return
    print ('[', node._item, ']', end = " ")
    self._print_preorder(node._left)
    self._print_preorder(node._right) 

class AdvBST4(AdvBST3):
    def printPreorderIterative(self):
        ret = []
        stack = [self._root]
        while stack:
            node = stack.pop()
            if node:
                ret.append(node._item)
                stack.append(node._right)
                stack.append(node._left)
        return ret

# 2.5 Iterative Postorder Traversal
# LRSelf顺序
# 记录访问过的记录状态
class AdvBST5(AdvBST4):
    def printPostorderIterative(self):
        node = self._root
        stack = []
        stack.append(node)
        
        while len(stack) != 0:
            node = stack[-1]
            if node._left is None and node._right is None:
                pop = stack.pop()
                print ('[', node._item, ']', end = " ")
                
            else:
                if node._right is not None:
                    stack.append(node._right)
                    node._right = None
                if node._left is not None:
                    stack.append(node._left)
                    node._left = None
        print('')

    def printPostorderIterative2(self):
        stack = [(self._root, False)]
        while stack:
            node, visited = stack.pop()
            if node:
                if visited:
                    # add to result if visited
                    print ('[', node._item, ']', end = " ")
                else:
                    # post-order
                    stack.append((node, True))
                    stack.append((node._right, False))
                    stack.append((node._left, False))

# 以上5道都是循环方式解题
# 类似链表

# 3.1 Level Order Traversal
# 用列表把下一层的节点顺序获得
# 查询节点下left和right并放到下层节点中
from collections import deque
class AdvBST1(BinarySearchTree):
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

# 3.2 Level Order Traversal I
# 把之前的结果集反向即可
# 或者插入文件的时候用insert放在0位
class AdvBST2(BinarySearchTree):
    
    def levelOrder(self):
        if not self._root:
            return []
        ans, level = [], [self._root]
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
        ans, level = [], [self._root]
        while level:
            ans.append([node._item for node in level])
            temp = []
            for node in level:
                temp.extend([node._left, node._right])
            level = [leaf for leaf in temp if leaf]
        ans.reverse()
        return ans    


# 3.3 Level Order Traversal III
# Binary Tree Zigzag Level Order Traversal
# 按照奇偶数设置flag+list切片末尾排序 用数字的正序逆序打印
class AdvBST3(AdvBST2):
    
    def zigzagLevelOrder(self,):
        if not self._root: 
            return []
        res, temp, stack, flag = [], [], [self._root], 1
        while stack:
            for i in range(len(stack)):
                node = stack.pop(0)
                temp += [node._item]
                if node._left:  stack += [node._left]
                if node._right: stack += [node._right]
            res += [temp[::flag]]
            temp = []
            flag *= -1
        return res


# 3.4 Construct Binary Tree from Preorder and Inorder Traversal
# 递归 用preorder作为指标 inorder不断依据node递归
# python用slice非常简单 方法2是不用python解法
def buildTree(preorder, inorder):
    if inorder:
        ind = inorder.index(preorder.pop(0))
        root = Node(inorder[ind])
        root._left = buildTree(preorder, inorder[0:ind])
        root._right = buildTree(preorder, inorder[ind+1:])
        return root

def buildTree2(preorder, inorder, preorderStart = 0, preorderEnd = None, inorderStart = 0, inorderEnd = None):
    if preorderEnd is None:
        preorderEnd = len(preorder) - 1
        
    if inorderEnd is None:
        inorderEnd = len(inorder) - 1

    if preorderStart > len(preorder) - 1 or inorderStart > inorderEnd:
        return None

    rootValue = preorder[preorderStart]
    root = Node(rootValue)
    inorderIndex = inorder.index(rootValue)

    root._left = buildTree2(preorder, inorder, preorderStart+1, inorderIndex, inorderStart, inorderIndex-1)
    root._right = buildTree2(preorder, inorder, preorderStart+inorderIndex+1-inorderStart, preorderEnd, inorderIndex+1, inorderEnd)

    return root


# 3.5 Construct Binary Tree from Inorder and Postorder Traversal
# 
def buildTree3(inorder, postorder):
    if not inorder or not postorder:
        return None

    root = Node(postorder.pop())
    inorderIndex = inorder.index(root._item)

    root._right = buildTree3(inorder[inorderIndex+1:], postorder)
    root._left = buildTree3(inorder[:inorderIndex], postorder)

    return root

# 3.6 Convert Sorted Array to Binary Search Tree
# 排好序创建平衡树
# 找到node再递归左右
# bst一半用递归一半用stack
def sortedArrayToBST(num):
    if not num:
        return None

    mid = len(num) // 2

    root = Node(num[mid])
    root._left = sortedArrayToBST(num[:mid])
    root._right = sortedArrayToBST(num[mid+1:])

    return root

# 3.7 Convert Sorted List to Binary Search Tree
from LinkedList import LinkedList as LL
from LinkedList import Node as LN
def sortedListToBST(head):
    if head is None:
        return None
    
    dummy = LN(0)
    dummy.next = head
    head = dummy
    
    fast = head
    slow = head
    left_tail = head
    
    while fast is not None and fast.next is not None:
        fast = fast.next.next
        left_tail = slow
        slow = slow.next
    
    left_tail.next = None
    node = Node(slow.value)
    node._left = sortedListToBST(head.next)
    node._right = sortedListToBST(slow.next)
    return node 


# 4.1 Path Sum
# 必须根到叶子（最低端） 没说二叉搜索 有可能有负数
# 不用太多复杂想法 记得最后递归是or来获得“可能”
from BinarySearchTree import BinarySearchTree 
from BinarySearchTree import Node
class AdvBST1(BinarySearchTree):
    def hasPathSumHelper(self, node, s):
        if not node:
            return False

        if not node._left and not node._right and node._item == s:
            return True
        
        s -= node._item

        return self.hasPathSumHelper(node._left, s) or self.hasPathSumHelper(node._right, s)
    
    def hasPathSum(self, s):
        return self.hasPathSumHelper(self._root, s)


# 4.2 Path Sum II
# 给出路径
class AdvBST2(AdvBST1):
    def hasPathSum2Helper(self, node, s):
        if not node:
            return []
        if not node._left and not node._right and s == node._item:
            return [[node._item]]
        tmp = self.hasPathSum2Helper(node._left, s-node._item) + self.hasPathSum2Helper(node._right, s - node._item)
        return [[node._item]+i for i in tmp]
    
    def hasPathSum2(self, s):
        return self.hasPathSum2Helper(self._root, s)    

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
            self.dfs(node._left, s-node._item, ls+[node._item], res)
        if node._right:
            self.dfs(node._right, s-node._item, ls+[node._item], res)



# 4.3 Path Sum III
# 一条上的路径 不要求根出发
# 返回路径数即可 具体量太大
class AdvBST4(AdvBST3):
    def findPathsHelper(self, node, target):
        if node:
            return int(node._item == target) + \
                self.findPathsHelper(node._left, target-node._item) + \
                self.findPathsHelper(node._right, target-node._item)
        return 0

    def pathSum(self, node, s):
        if node:
            return self.findPathsHelper(node, s) + self.pathSum(node._left, s) + self.pathSum(node._right, s)
        return 0
    
    def findPaths(self, target):
        return self.findPathsHelper(self._root, target)       


# 4.4 First Common Ancestor for Binary Search Tree
# 找到两节点最近共同祖先
# 从根节点出发判断根节点再移动根节点 在两侧时候即可
class AdvBST5(AdvBST4):
    def lowestCommonAncestor(self, p, q):
        return self.lowestCommonAncestorHelper(self._root, p, q)
    
    def lowestCommonAncestorHelper(self, node, p, q):
        while node:
            if node._item > p._item and node._item > q._item:
                node = node._left
            elif node._item < p._item and node._item < q._item:
                node = node._right
            else:
                return node






