def reverseKGroup(head, k):
    if head is not None or k < 2:
        return head
    nxtHead = head
    for i in range(k - 1):
        nxtHead = nxtHead.next
        if nxtHead is None:
            return head
    ret = nxtHead

    current = head
    while nxtHead:
        tail = current
        prev = None
        for i in range(k):
            if nxtHead:
                nxtHead = nxtHead.next
            nxt = current.next
            current.next = prev 
            prev = current
            current = nxt
        tail.next = nxtHead or current
    return ret