# 18.2 图形问题总结
# DFS用stack访问内容 还可以递归
# BFS用deque 依次访问后面的内容
# 三个程序的内容必须巩固 前三天一天写一遍
# 时间复杂度都是e+v

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
# 有没有终点直接用dfs 
# 如何记录下个节点 stack recursion
# 如何记录已访问节点 set matrix
# 如何记录路径 dict
# 第一个必须其余两个未必
# 递归做法没有规定必须往哪里走
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
# 此处是stack的pop换成queue的popleft
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
# 横冲直撞到碰墙回头的路线最终的位置
# 寻找neighbor方法不同
# 此处用while想到上面的内容
def dfs2(matrix, start, dest):
    visited = [[False] * len(matrix[0]) for i in range(len(matrix))]
    return dfsHelper2(matrix, start, dest, visited)
    
def dfsHelper2(matrix, start, dest, visited):
    if matrix[start[0]][start[1]] == 1:
        return False
    
    if visited[start[0]][start[1]]:
        return False
    if start[0] == dest[0] and start[1] == dest[1]:
        return True
    
    visited[start[0]][start[1]] = True
    
    r = start[1] + 1
    l = start[1] - 1
    u = start[0] - 1
    d = start[0] + 1
    
    while (r < len(matrix[0]) and matrix[start[0]][r] == 0):  ##  right
        r += 1
    x = (start[0], r - 1)
    if (dfsHelper2(matrix, x, dest, visited)):
        return True

    while (l >= 0 and matrix[start[0]][l] == 0):  ##  left
        l -= 1
    x = (start[0], l + 1)
    if (dfsHelper2(matrix, x, dest, visited)):
        return True
    
    while (u >= 0 and matrix[u][start[1]] == 0): ##  up
        u -= 1
    x = (u + 1, start[1])
    if (dfsHelper2(matrix, x, dest, visited)):
        return True
        
    while (d < len(matrix) and matrix[d][start[1]] == 0): ##  down
        d += 1
    x = (d - 1, start[1])
    if (dfsHelper2(matrix, x, dest, visited)):
        return True
            
    return False


# 1.3 The Maze III
# 找最短路径都用bfsv只能用for循环
# 调用neighbor可调节方向
import heapq
def shortestDistance(matrix, start, destination):
    def neighbors(matrix, node):
        for dir in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
            cur_node, dist = list(node), 0
            while 0 <= cur_node[0] + dir[0] < len(matrix) and \
                  0 <= cur_node[1] + dir[1] < len(matrix[0]) and \
                  matrix[cur_node[0] + dir[0]][cur_node[1] + dir[1]] == 0:
                cur_node[0] += dir[0]
                cur_node[1] += dir[1]
                dist += 1
            yield dist, tuple(cur_node)

    heap = [(0, start)]
    visited = set()
    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited: continue
        if node == destination:
            return dist
        visited.add(node)
        for neighbor_dist, neighbor in neighbors(matrix, node):
            heapq.heappush(heap, (dist + neighbor_dist, neighbor))

    return -1


# 1.4 The Maze IV
# 打印路径必须用dict 此时矩阵只要有上下左右就可以知道怎么走可以用string
import heapq
def findShortestWay(maze, ball, hole):
    dirs = {'u' : (-1, 0), 'r' : (0, 1), 'l' : (0, -1), 'd': (1, 0)}

    def neighbors(maze, node):
        for dir, vec in dirs.items():
            cur_node, dist = list(node), 0
            while 0 <= cur_node[0]+vec[0] < len(maze) and \
                  0 <= cur_node[1]+vec[1] < len(maze[0]) and \
                  not maze[cur_node[0]+vec[0]][cur_node[1]+vec[1]]:
                cur_node[0] += vec[0]
                cur_node[1] += vec[1]
                dist += 1
                if tuple(cur_node) == hole:
                    break
            yield tuple(cur_node), dir, dist

    heap = [(0, '', ball)]
    visited = set()
    while heap:
        dist, path, node = heapq.heappop(heap)
        if node in visited: continue
        if node == hole: return path
        visited.add(node)
        for neighbor, dir, neighbor_dist in neighbors(maze, node):
            heapq.heappush(heap, (dist+neighbor_dist, path+dir, neighbor))

    return "impossible"


# 2.1 Flood Fill
# 找到相连并且替换颜色 找到就是true/false就是dfs 
# 在改掉颜色后也不产生影响继续找邻居 
# 颜色不相等的判断就是看有没有访问过
def floodFill(image, sr, sc, newColor):
    rows, cols, orig_color = len(image), len(image[0]), image[sr][sc]
    def traverse(row, col):
        if (not (0 <= row < rows and 0 <= col < cols)) or image[row][col] != orig_color:
            return
        image[row][col] = newColor
        [traverse(row + x, col + y) for (x, y) in ((0, 1), (1, 0), (0, -1), (-1, 0))]
    if orig_color != newColor:
        traverse(sr, sc)
    return image


# 2.2 Friend Circles
# 首先考虑对每个人形成的矩阵进行遍历
# 再对已经遍历的每个人的位置做出动作
def findCircleNum(M):
    circle = 0
    n = len(M)
    for i in range(n):
        if M[i][i] != 1:
            continue
        friends = [i]
        while friends:
            f = friends.pop()
            if M[f][f] == 0:
                continue
            M[f][f] = 0
            for j in range(n):
                if M[f][j] == 1 and M[j][j] == 1:
                    friends.append(j)
        circle += 1
    return circle

def findCircleNum2(M):
    def dfs(node):
        visited.add(node)
        for friend in range(len(M)):
            if M[node][friend] and friend not in visited:
                dfs(friend)

    circle = 0
    visited = set()
    for node in range(len(M)):
        if node not in visited:
            dfs(node)
            circle += 1
    return circle


# 2.3 Number of Islands
# 只可能去找每个点
# 运行两次dfs
def numIslands(grid):
    if not grid:
        return 0
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                dfs(grid, i, j)
                count += 1
    return count

def dfs(grid, i, j):
    if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] != 1:
        return
    grid[i][j] = '#'
    dfs(grid, i + 1, j)
    dfs(grid, i - 1, j)
    dfs(grid, i, j + 1)
    dfs(grid, i, j - 1)


# 2.4 Max Area of Island
# 求每个岛的面积最终找最大的
# 那就是现在对每个点dfs并且记录面积 那就是每次调用成功就+1
# global Max可以记录下来
def maxAreaOfIsland(grid):
    m, n = len(grid), len(grid[0])

    def dfs(i, j):
        if 0 <= i < m and 0 <= j < n and grid[i][j]:
            grid[i][j] = 0
            return 1 + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i + 1, j) + dfs(i, j - 1)
        return 0

    result = 0
    for x in range(m):
        for y in range(n):
            if grid[x][y]:
                result = max(result, dfs(x, y))
    return result


# 2.5 Employee Importance
# 自定义class就是个holder
# 再把所有的都放到一个数组里面再包装
# 如同寻找bst的size 可以比较观察 递归很多时候就dfs
class Employee(object):
    def __init__(self, id, importance, subordinates):
        # It's the unique id of each node.
        # unique id of this employee
        self.id = id
        # the importance value of this employee
        self.importance = importance
        # the id of direct subordinates
        self.subordinates = subordinates
e3 = Employee(3, 3, [])
e2 = Employee(2, 3, [])
e1 = Employee(1, 5, [2, 3])
emps = [e1, e2, e3]
def getImportance(employees, id):
    table = {emp.id: emp for emp in employees}

    def dfs(emp):
        if emp.subordinates == []:  # base case
            return emp.importance
        else:  # recursive case
            value = emp.importance
            for sub in emp.subordinates:
                value += dfs(table[sub])
            return value
            # or just:
            # return emp.importance + sum(dfs(table[sub]) for sub in emp.subordinates)

    return dfs(table[id])


def getImportance2(employees, id):
    value = 0
    table = {}
    for emp in employees:
        table[emp.id] = emp

    stack = [table[id]]

    while stack:
        emp = stack.pop()
        for sub in emp.subordinates:
            stack.append(table[sub])
        value += emp.importance

    return value


# 3.1 Is Graph Bipartite?
# 二分图 
# 列出项目内容给出
def isBipartite(graph):
    color = {}
    def dfs(pos):
        for i in graph[pos]:
            if i in color:
                if color[i] == color[pos]: return False
            else:
                color[i] = color[pos] ^ 1
                if not dfs(i): return False
        return True
    
    for i in range(len(graph)):
        if i not in color: color[i] = 0
        if not dfs(i): return False
    return True


# 3.2 Pacific Atlantic Water Flow
# 反着推算是不是可以追回到上面去 看横纵两排可以取到的点做set 两个set做交集
# 简化方法是上来先把所有的横纵边缘点放到stack里面做bfs
def pacificAtlantic(matrix):
    if not matrix: return []
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    m = len(matrix)
    n = len(matrix[0])
    p_visited = [[False for _ in range(n)] for _ in range(m)]

    a_visited = [[False for _ in range(n)] for _ in range(m)]
    result = []

    for i in range(m):
        # p_visited[i][0] = True
        # a_visited[i][n-1] = True
        dfs(matrix, i, 0, p_visited, m, n)
        dfs(matrix, i, n-1, a_visited, m, n)
    for j in range(n):
        # p_visited[0][j] = True
        # a_visited[m-1][j] = True
        dfs(matrix, 0, j, p_visited, m, n)
        dfs(matrix, m-1, j, a_visited, m, n)

    for i in range(m):
        for j in range(n):
            if p_visited[i][j] and a_visited[i][j]:
                result.append([i,j])
    return result

def dfs(matrix, i, j, visited, m, n):
    # when dfs called, meaning its caller already verified this point 
    visited[i][j] = True
    for dir in [(1,0),(-1,0),(0,1),(0,-1)]:
        x, y = i + dir[0], j + dir[1]
        if x < 0 or x >= m or y < 0 or y >= n or visited[x][y] or matrix[x][y] < matrix[i][j]:
            continue
        dfs(matrix, x, y, visited, m, n)

from collections import deque
def pacificAtlantic(matrix):
    if not matrix: return []
    m, n = len(matrix), len(matrix[0])
    def bfs(reachable_ocean):
        q = deque(reachable_ocean)
        while q:
            (i, j) = q.popleft()
            for (di, dj) in [(0,1), (0, -1), (1, 0), (-1, 0)]:
                if 0 <= di+i < m and 0 <= dj+j < n and (di+i, dj+j) not in reachable_ocean \
                    and matrix[di+i][dj+j] >= matrix[i][j]:
                    q.append( (di+i,dj+j) )
                    reachable_ocean.add( (di+i, dj+j) )
        return reachable_ocean         
    pacific  =set ( [ (i, 0) for i in range(m)]   + [(0, j) for j  in range(1, n)]) 
    atlantic =set ( [ (i, n-1) for i in range(m)] + [(m-1, j) for j in range(n-1)]) 
    return list( bfs(pacific) & bfs(atlantic) )


# 3.3 Longest Increasing Path in a Matrix
# 把之前结果存储起来的动态规划想法
def longestIncreasingPath(matrix):
    if not matrix: return 0
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    m = len(matrix)
    n = len(matrix[0])
    cache = [[-1 for _ in range(n)] for _ in range(m)]
    res = 0
    for i in range(m):
        for j in range(n):
            cur_len = dfs(i, j, matrix, cache, m, n)
            res = max(res, cur_len)
    return res

def dfs(i, j, matrix, cache, m, n):
    if cache[i][j] != -1:
        return cache[i][j]
    res = 1
    for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
        x, y = i + direction[0], j + direction[1]
        if x < 0 or x >= m or y < 0 or y >= n or matrix[x][y] <= matrix[i][j]:
            continue
        length = 1 + dfs(x, y, matrix, cache, m, n)
        res = max(length, res)
    cache[i][j] = res
    return res


# 3.4 01 Matrix
# 距离场 直接就是djiska或者bfs
def updateMatrix(matrix):
    q, m, n = [], len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(n):
            if matrix[i][j] != 0:
                matrix[i][j] = 0x7fffffff
            else:
                q.append((i, j))
    for i, j in q:
        for r, c in ((i, 1+j), (i, j-1), (i+1, j), (i-1, j)):
            z = matrix[i][j] + 1
            if 0 <= r < m and 0 <= c < n and matrix[r][c] > z:
                matrix[r][c] = z
                q.append((r, c))
    return matrix
# 从左上右下两个方向进入
def updateMatrix2(matrix):
    def DP(i, j, m, n, dp):
        if i > 0: dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)
        if j > 0: dp[i][j] = min(dp[i][j], dp[i][j - 1] + 1)
        if i < m - 1: dp[i][j] = min(dp[i][j], dp[i + 1][j] + 1)
        if j < n - 1: dp[i][j] = min(dp[i][j], dp[i][j + 1] + 1)
            
    if not matrix: return [[]]
    m, n = len(matrix), len(matrix[0])
    dp = [[0x7fffffff if matrix[i][j] != 0 else 0 for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            DP(i, j, m, n, dp)

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            DP(i, j, m, n, dp)

    return dp


# 4.1 Accounts Merge
# 像员工重要度 要转化成图论
# 是用email作为顶点 用account作为边进行dfs
def accountsMerge(accounts):
    from collections import defaultdict
    visited_accounts = [False] * len(accounts)
    emails_accounts_map = defaultdict(list)
    res = []
    # Build up the graph.
    for i, account in enumerate(accounts):
        for j in range(1, len(account)): #email starts from 2nd
            email = account[j]
            emails_accounts_map[email].append(i)
            
    print(emails_accounts_map)
    # DFS code for traversing accounts.
    def dfs(i, emails):
        if visited_accounts[i]:
            return
        visited_accounts[i] = True
        for j in range(1, len(accounts[i])):
            email = accounts[i][j]
            emails.add(email)
            for neighbor in emails_accounts_map[email]:
                dfs(neighbor, emails)
    # Perform DFS for accounts and add to results.
    for i, account in enumerate(accounts):
        if visited_accounts[i]:
            continue
        name, emails = account[0], set()
        dfs(i, emails)
        res.append([name] + sorted(emails))
    return res


# 4.2 Word Ladder 
# 搜索题目很多可以用图论
# 构建图论的核心是找到neighbor
from collections import deque
def ladderLength(beginWord, endWord, wordList):
    wordSet=set(wordList)
    wordSet.add(endWord)
    queue = deque([[beginWord, 1]])
    while queue:
        word, length = queue.popleft()
        if word == endWord:
            return length
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                if next_word in wordSet:
                    wordSet.remove(next_word)
                    queue.append([next_word, length + 1])
    return 0


# 4.3 Word Ladder II
# 找出所有内容的最短路径
from collections import defaultdict
import string
def findLadders(start, end, wordList):
    dic = set(wordList)
    dic.add(end)
    level = {start}
    parents = defaultdict(set)
    while level and end not in parents:
        next_level = defaultdict(set)
        for node in level:
            for char in string.ascii_lowercase:
                for i in range(len(start)):
                    n = node[:i] + char + node[i+1:]
                    if n in dic and n not in parents:
                        next_level[n].add(node)
        level = next_level
        parents.update(next_level)
    res = [[end]]
    print(parents)
    while res and res[0][0] != start:
        res = [[p]+r for r in res for p in parents[r[0]]]
    return res


# 拓扑排序
# 每个点计算多少个incoming edge然后使用
