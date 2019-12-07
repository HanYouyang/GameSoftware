def mergeTwoLists(l1, l2):
    dum = cur = Node(0)
    while l1 and l2:
        if l1.value < l2.value:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dum.next
def mergeTwoLists2(l1, l2):
    if not l1 or not l2:
        return l1 or l2
    if l1.value < l2.value:
        l1.next = mergeTwoLists2(l1.next, l2)
        return l1
    else:
        l2.next = mergeTwoLists2(l1, l2.next)
        return l2