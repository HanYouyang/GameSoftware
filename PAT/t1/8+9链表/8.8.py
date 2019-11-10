def delete_node(node):
    print(node.value)
    node.value = node.next.value
    node.next = node.next.next

def find_middle(lst):
    assert lst.head is not None and lst.head.next is not None

    head = lst.head
    fast = head
    slow = head

    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
    
    return slow.next

