def split(head):
    if head is None:
        return
    
    slow = head
    fast = head 
    fron_last_node = slow

    while fast is not None:
        fron_last_node = slow
        slow = slow.next
        fast = fast.next.next if fast.next is not None else None
    fron_last_node.next = None
    front = head
    back = slow

    return front, back