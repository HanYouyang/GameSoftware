def remove_nth(lst, n):
    assert n <= lst.length and n > 0

    fast = lst.head
    while n > 0:
        fast = fast.next
        n = n - 1

    slow = lst.head
    while fast.next is not None:
        fast = fast.next
        slow = slow.next
    
    result = slow.next
    slow.next = slow.next.next

    lst.length = lst.length - 1
    
    return result
