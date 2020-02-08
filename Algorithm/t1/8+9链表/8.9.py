def has_cycle(lst):
    return has_cycle_helper(lst.head)

def has_cycle_helper(head):
    if head is None:
        return False
    
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
        if slow == fast:
            return True
    
    return False
