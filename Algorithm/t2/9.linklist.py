# 01 
# 学会使用head pre cur nxt tail
# 1 删除节点
# 除了尾部 只允许访问自己的节点 
def deleteNode(node):
    print(node.value)
    node.value = node.next.value
    node.next = node.next.next

# 2.1 找到中间节点
# 1.sll双指针 一个走得快一个走的慢
# 2.dll相向穿过
# 一定注意不能出现null避免出现空
def findMiddle(lst):
    assert lst.head is not None and lst.head.next is not None
    head = lst.head
    fast = head
    slow = head
    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
    return slow.value

# 2.2 判断有环
# 双指针 肯定是套圈
def hasCycle(lst):
    return hasCycleHelper(lst.head)
def hasCycleHelper(head):
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

# 2.3 找环的起点
# 双指针
# fast双倍速那就是倒退情况走2k相遇 这是相遇点的计算方法
# 假设环起始距离直线k则fast已经走到2k环上 
# 倒退k距离获得环上起点两者也必然相遇在这里
# 此时安排f和l一个在相遇点一个在直线起点行进 再次相遇是起点
def findBeginning(head):
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
    if fast is None or fast.next is None:
        return None
    while fast != slow:
        fast = fast.next
        slow = slow.next
    return slow

# 2.4 删除倒数第N点
# 双指针 直接差N即可
def removeNth(lst, n):
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

# 2.5 分半 其实应该放在dm2
# 双指针
# 先找中间数字再分割
# 设置dmh2 中间为空 开始为dmh1
def split(head):
    if (head is None):
        return
    slow = head
    fast = head
    front_last_node = slow
    while (fast is not None):
        front_last_node = slow
        slow = slow.next
        fast = fast.next.next if fast.next is not None else None
    front_last_node.next = None
    front = head
    back = slow
    return (front, back)

# 02
# 链表是哈希表和缓存用到
from LinkedList import LinkedList
from LinkedList import Node
# 1 合并两个链表
# 双指针 相比数组不用额外空间
# 1.循环写法
# 2.递归写法
def mergeTwoLists1(l1, l2):
    dummy = cur = Node(0)
    while l1 and l2:
        if l1.value < l2.value:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next
def mergeTwoLists2(l1, l2):
    if not l1 or not l2:
        return l1 or l2
    if l1.value < l2.value:
        l1.next = mergeTwoLists2(l1.next, l2)
        return l1
    else:
        l2.next = mergeTwoLists2(l1, l2.next)
        return l2

# 2 找两个链表共同起点
# 1.先找各自长度再找各自长度差开始比较是否相同
# 2.先遍历知道走到终点互换位置再相遇跑同样长度
def getIntersectionNode(headA, headB):
    curA, curB = headA, headB
    lenA, lenB = 0, 0
    while curA is not None:
        lenA += 1
        curA = curA.next
    while curB is not None:
        lenB += 1
        curB = curB.next
    curA, curB = headA, headB
    if lenA > lenB:
        for i in range(lenA-lenB):
            curA = curA.next
    elif lenB > lenA:
        for i in range(lenB-lenA):
            curB = curB.next
    while curB != curA:
        curB = curB.next
        curA = curA.next
    return curA

# 3.1 插入排序
# 先建立dm pre cur 
# dm不动 pre循链找到合适元素指向前调 cur最先放到前调下面
def insertionSortList(head):
    dummy = Node(0)
    cur = head
    # pre is the sorted part
    # when see a new node, start from dummy
    # cur is the unsorted part
    while cur is not None:
        pre = dummy
        while pre.next is not None and pre.next.value < cur.value:
            pre = pre.next
        temp = cur.next
        cur.next = pre.next
        pre.next = cur
        cur = temp
    return dummy.next

# 3.2 排序链表
# tonlgn 实则要求分治法 先拆分再合并
# 拆分是昨天最后题目 合并是今天最早题目 拆分前提是找到中点也有
def sortList(head):
    if head is None or head.next is None:
        return head
    mid = getMiddle(head)
    rHead = mid.next
    mid.next = None
    return merge(sortList(head), sortList(rHead))
def merge(lHead, rHead):
    dummyNode = dummyHead = Node(0)
    while lHead and rHead:
        if lHead.value < rHead.value:
            dummyHead.next = lHead
            lHead = lHead.next
        else:
            dummyHead.next = rHead
            rHead = rHead.next
        dummyHead = dummyHead.next
    if lHead:
        dummyHead.next = lHead
    elif rHead:
        dummyHead.next = rHead
    return dummyNode.next
def getMiddle(head):
    if head is None:
        return head
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# 3.3 分割链表
# 从前往后走的快速排序分割 形成快排还要递归调用
# 建立两个ld和rd比较值再连起来
# 注意最后是连上rd.next
def partition(head, x):
    leftHead = Node(None)  # head of the list with nodes values < x
    rightHead = Node(None)  # head of the list with nodes values >= x
    left = leftHead  # attach here nodes with values < x
    right = rightHead  # attach here nodes with values >= x
    # traverse the list and attach current node to left or right nodes
    while head:
        if head.value < x:
            left.next = head
            left = left.next
        else:  # head.val >= x
            right.next = head
            right = right.next
        head = head.next
    right.next = None  # set tail of the right list to None
    left.next = rightHead.next  # attach left list to the right
    return leftHead.next  # head of a new partitioned list

# 03
# 1.1 翻转链表
# inplace 
def reverse(lst):
    head = lst.head
    result = None
    current = head.next
    nxt = None
    while current is not None:
        nxt = current.next
        current.next = result
        result = current
        current = nxt
    head.next = result
def reverseRecursion(node):
    if (node is None or node.next is None):
        return node
    p = reverseRecursion(node.next)
    node.next.next = node
    node.next = None
    return p

# 1.2 翻转链表2
# 给定位置翻转
# 比刚才多用两个变量
def reverseBetween(head, m, n):
    if m == n:
        return head
    dummyNode = Node(0)
    dummyNode.next = head
    pre = dummyNode
    for i in range(m - 1):
        pre = pre.next
    # reverse the [m, n] nodes
    result = None
    current = pre.next
    for i in range(n - m + 1):
        nxt = current.next
        current.next = result
        result = current
        current = nxt
    pre.next.next = current
    pre.next = result
    return dummyNode.next

# 1.3 翻转链表3
# 交换相邻的链表元素
def swapPairs(head):
    dummy = cur = Node(0)
    dummy.next = head
    while cur.next and cur.next.next:
        p1 = cur.next
        p2 = cur.next.next
        cur.next = p2
        p1.next = p2.next
        p2.next = p1
        cur = cur.next.next
    return dummy.next

# 1.4 翻转链表4
# 分k个一组翻转
def reverseKGroup(head, k):
    if head is None or k < 2:
        return head
    next_head = head
    for i in range(k - 1):
        next_head = next_head.next
        if next_head is None:
            return head
    ret = next_head
    current = head
    while next_head:
        tail = current
        prev = None
        for i in range(k):
            if next_head:
                next_head = next_head.next
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt
        tail.next = next_head or current
    return ret

# 2 回文链表
# 先找到中间点 再依次翻转 最后部分翻转 拆分链表
def isPalindrome(head):
    rev = None
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        rev, rev.next, slow = slow, rev, slow.next
    if fast:
        slow = slow.next
    while rev and rev.value == slow.value:
        slow = slow.next
        rev = rev.next
    return not rev

# 3.1 删除重复
# cur nxt 直接比较值不然就连接下面的
def deleteDuplicates(head):
    if head == None:
        return head
    node = head
    while node.next:
        if node.value == node.next.value:
            node.next = node.next.next
        else:
            node = node.next
    return head

# 3.2 删除重复2
# 重复的元素全部删除不包含已有元素
# 等到有不重复的才移动pre
def deleteDuplicates2(head):
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