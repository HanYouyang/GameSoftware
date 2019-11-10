def delDup(head):
    if head == None:
        return head
    node = head

    while node.next:
        if node.value == node.next.value:
            node.next = node.next.next
        else:
            node = node.next
        
    return head

def delDup2(head):
    dummy = pre = Node(0)
    dummy.next = head
    while head and head.next:
        if head.value == head.next.value:
            while head and head.next and head.value == head.next.value:
                head = head.next
            head = head.next
            pre.next = head
        else:
            pre = pre.next
            head = head.next
    return dummy.next