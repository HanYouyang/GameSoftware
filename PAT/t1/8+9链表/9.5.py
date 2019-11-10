def insertSortList(head):
    dummy = Node(0)
    cur = head
    while cur is not None:
        pre = dummy
        while pre.next is not None and pre.next.value < cur.value:
            pre = pre.next
        temp = cur.next
        cur.next = pre.next
        pre.next = cur
        cur = temp
    return dummy.next