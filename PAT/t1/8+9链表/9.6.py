class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None
        
class Solution(object):
    def getMiddle(self, head):
        if head is None:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow
    def merge(self, lHead, rHead):
        dummyNode = dummyHead = ListNode(0)
        while lHead and rHead:
            if lHead.val < rHead.val:
                dummyHead.next = lHead
                lHead = lHead.next
            else:
                dummyHead.next = rHead
                rHead = rHead.next
            dummyHead = dummyHead.nexts
        if lHead:
            dummyHead.next = lHead
        elif rHead:
            dummyHead.next = rHead
        return dummyNode.next
    
    def sortList(self, head):
        if head is None or head.next is None:
            return head
        mid = getMiddle(head)
        rHead = mid.next
        mid.next = None
        return merge(sortList(head), sortList(rHead))