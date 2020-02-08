def reverse(ll):
    head = ll.head
    pre = None
    current = head.next
    nxt = None

    while current is not None:
        nxt = current.next
        current.next = pre
        pre = current
        current = nxt

    head.next = pre

def reverRecursion(node):
    if node is None or node.next is None:
        return node
    p = reverRecursion(node.next)
    node.next.next = node
    node.next = None
    return p

