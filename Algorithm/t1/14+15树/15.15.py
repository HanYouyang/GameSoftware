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