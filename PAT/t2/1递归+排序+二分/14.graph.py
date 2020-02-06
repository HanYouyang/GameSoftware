# 18.2 图形问题总结
# DFS用stack访问内容 还可以递归
# BFS用deque 依次访问后面的内容
# 三个程序的内容必须巩固 前三天一天写一遍

# 最短路径用BFS 只考虑步数 但是还有权重表示各种内容
# Dijiska用heap 
# 不能解决负数 负循环更糟糕 Bellman-Ford 更新每一次的距离 实时更新
# 不考虑终点 A*算法 用尽可能靠近终点的范围
def dfs(G, currentVert, visited):
    visited[currentVert] = True  # mark the visited node 
    print("traversal: " + currentVert.getVertexID())
    for nbr in currentVert.getConnections():  # take a neighbouring node 
        if nbr not in visited:  # condition to check whether the neighbour node is already visited
            dfs(G, nbr, visited)  # recursively traverse the neighbouring node
    return 
 
def DFSTraversal(G):
    visited = {}  # Dictionary to mark the visited nodes 
    for currentVert in G:  # G contains vertex objects
        if currentVert not in visited:  # Start traversing from the root node only if its not visited 
            dfs(G, currentVert, visited)  # For a connected graph this is called only onc

def dfsIterative(G, start, dest):
    stack = [] # vertex
    visited = set() # vertex id
    parent = {} # vertex id
    stack.append(start)
    while len(stack) != 0:
        curr = stack.pop() # vertex
        print("visiting ", curr.getVertexID())
        if (curr.getVertexID() == dest.getVertexID()):
            return parent
        neighbors = G.getNeighbors(curr.getVertexID())
        for n in neighbors:
            id = n.getVertexID()
            visited.add(id)
            parent[id] = curr.getVertexID()
            stack.append(n)
    return None


from collections import deque
def bfs(G, start, dest):
    queue = deque() # vertex
    visited = set() # vertex id
    parent = {} # vertex id
    queue.append(start)
    while len(queue) != 0:
        curr = queue.popleft() # vertex
        print("visiting ", curr.getVertexID())
        if (curr.getVertexID() == dest.getVertexID()):
            return parent
        neighbors = G.getNeighbors(curr.getVertexID())
        for n in neighbors:
            id = n.getVertexID()
            visited.add(id)
            parent[id] = curr.getVertexID()
            queue.append(n)
    return None


# 1.1 The Maze 
# 迷宫直接用dfs 
# 如何记录下个节点 stack recursion
# 如何记录已访问节点 set matrix
# 如何记录路径 dict
# 第一个必须其余两个未必
from AdjListGraph import Graph
from AdjListGraph import Vertex
def dfs(matrix, start, dest):
    visited = [[False] * len(matrix[0]) for i in range(len(matrix))]
    return dfsHelper(matrix, start, dest, visited)
    
def dfsHelper(matrix, start, dest, visited):
    if matrix[start[0]][start[1]] == 1:
        return False
    
    if visited[start[0]][start[1]]:
        return False
    if start[0] == dest[0] and start[1] == dest[1]:
        return True
    
    visited[start[0]][start[1]] = True
    
    if (start[1] < len(matrix[0]) - 1):
        r = (start[0], start[1] + 1)
        if (dfsHelper(matrix, r, dest, visited)):
            return True
        
    if (start[1] > 0):
        l = (start[0], start[1] - 1)
        if (dfsHelper(matrix, l, dest, visited)):
            return True
        
    if (start[0] > 0):
        u = (start[0] - 1, start[1])
        if (dfsHelper(matrix, u, dest, visited)):
            return True
        
    if (start[0] < len(matrix[0]) - 1):
        d = (start[0] + 1, start[1])
        if (dfsHelper(matrix, d, dest, visited)):
            return True
            
    return False
# for循环代替四个方向
def dfsIterative(matrix, start, dest):
    visited = [[False] * len(matrix[0]) for i in range(len(matrix))]
    stack = []
    stack.append(start)
    visited[start[0]][start[1]] = True
    
    idxs = [[0,1], [0,-1], [-1,0], [1,0]]
    
    while len(stack) != 0:
        curr = stack.pop() # vertex
        if (curr[0] == dest[0] and curr[1] == dest[1]):
            return True

        for idx in idxs:
            x = curr[0] + idx[0]
            y = curr[1] + idx[1]
            
            if (x < 0 or x >= len(matrix) or y < 0 or y >= len(matrix[0])):
                continue
            
            if (matrix[x][y] == 1):
                continue
                
            if (visited[x][y] == True):
                continue
            visited[x][y] = True
            stack.append((x, y))
            
    return False
# 
from collections import deque

def bfs(matrix, start, dest):
    visited = [[False] * len(matrix[0]) for i in range(len(matrix))]
    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True
    
    idxs = [[0,1], [0,-1], [-1,0], [1,0]]
    
    while len(queue) != 0:
        curr = queue.popleft() # vertex
        if (curr[0] == dest[0] and curr[1] == dest[1]):
            return True

        for idx in idxs:
            x = curr[0] + idx[0]
            y = curr[1] + idx[1]
            
            if (x < 0 or x >= len(matrix) or y < 0 or y >= len(matrix[0])):
                continue
            
            if (matrix[x][y] == 1):
                continue
                
            if (visited[x][y] == True):
                continue
            visited[x][y] = True
            queue.append((x, y))
            
    return False


# 1.2 The Maze II
# 
# 
# 
# 














