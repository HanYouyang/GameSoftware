def partition(head, x):
    lHead = Node(None)
    rHead = Node(None)
    l = lHead
    r = rHead

    while head is not None:
        if head.value < x:
            l.next = head
            l = l.next
        else:
            r.next = head
            r = r.next
        head = head.next
    r.next = None
    l.next = rHead.next
    return lHead.next