def buildTree(preorder, inorder):
    if inorder:
        ind = inorder.index(preorder.pop(0))
        root = Node(inorder[ind])
        root._left = buildTree(preorder, inorder[0 : ind])
        root._right = buildTree(preorder, inorder[ind + 1 : ])
        return root

def buildTree2(inorder, postorder):
    if not inorder or not postorder:
        return None
    
    root = Node(postorder.pop())
    inorderIndex = inorder.index(root._item)

    root._right = buildTree2(inorder[inorderIndex + 1 : ], postorder)
    root._left = buildTree2(inorder[ : inorderIndex], postorder)

    return root
