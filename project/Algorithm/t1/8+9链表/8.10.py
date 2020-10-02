def find_beginning(head):
    if head is None:
        return None
    
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next

        if slow == fast:
            fast = head
            break

    if fast is None and fast.next is None:
        return None
    
    while fast != slow:# 这时候改变了所谓fast的速度两者同速前行
        fast = fast.next
        slow = slow.next
    
    return slow
