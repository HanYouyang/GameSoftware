import heapq

def shorteseDistance(matrix, start, destination):
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
    