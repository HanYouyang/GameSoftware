def reverseFrom(head, m, n):
    if m == n:
        return head
    dumNode = Node(0)
    dumNode.next = head
    first = dumNode
    
    for i in range(m - 1):
        first = first.next
    
    pre = None
    current = first.next
    for i in range(n - m + 1):
        nxt = current.next
        current.next = pre
        pre = current
        current = nxt

    third = nxt
    first.next.next = third
    second = pre
    first.next = second

    return dumNode.next