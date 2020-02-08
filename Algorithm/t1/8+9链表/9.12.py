def isPalidrome(head):
    rev = None
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        rev, rev.next, slow  = slow, rev, slow.next
    
    if fast:
        slow = slow.next
    while rev and rev.value == slow.value:
        slow = slow.next
        rev = rev.next
    return not rev
    