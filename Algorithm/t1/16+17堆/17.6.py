from queue import PriorityQueue
from LinkedList import LinkedList
from LinkedList import Node

def mergeKLists(lists):# 此处lists包含几个链表
    dummy = Node(None)
    curr = dummy
    q = PriorityQueue()
    for node in lists:
        if node:
            q.put((node.value, node))
    while q.qsize() > 0:
        curr.next = q.get()[1]
        curr = curr.next
        if curr.next:
            q.put((curr.next.value, curr.next))
    return dummy.next