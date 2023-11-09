import queue
import enum
from collections import deque
from tkinter.tix import INTEGER
import sys

class V(enum.Enum):
    NOT_VISITED = 0     # state is not visited yet
    FRONTIER = 1        # state is in frontier
    VISITED = 2        # state is explored already


def search_A(graph, start, goal):
    min_distance = dict()
    maxValue = int(10000000)
    for state in graph:
        min_distance[state] = maxValue

    node = (heuristic(start, goal), start, None)  
    frontier = queue.PriorityQueue()
    explored = [] #luu lai duong di
    min_distance[start] = heuristic(start, goal) 

    frontier.put(node)

    while frontier.queue:
        nodeFirst = frontier.get()
        
        if nodeFirst[0] > min_distance[nodeFirst[1]]:
            continue #skip 
        
        explored.append((nodeFirst[1], nodeFirst[2])) #thêm vào đường đi 
        if nodeFirst[1] == goal:      
            return get_path(explored)    # success
        for child_state in graph[nodeFirst[1]]: #danh sach ke
            h_state = heuristic(nodeFirst[1], goal)
            h_child_score = heuristic(child_state, goal)
            prev_distance = nodeFirst[0] - h_state
            h_score = prev_distance + 1 + h_child_score
            if min_distance[child_state] > h_score:
                min_distance[child_state] = h_score
                frontier.put((min_distance[child_state], child_state, nodeFirst[1])) 
    return None     # failure


def search_BFS(graph, start, goal) :
    visited = dict()
    for state in graph :
        visited[state] = V.NOT_VISITED #Khoi tao trang thai ban dau
    queueBfs = queue.Queue()
    node  = (start, None)
    queueBfs.put(node)
    # tao mang luu tien trinh
    explored = []
    
    while not queueBfs.empty():
        nodeCur = queueBfs.get()
        # already visited
        visited[nodeCur[0]] = V.VISITED
        #save road
        explored.append((nodeCur[0], nodeCur[1]))
        
        # check successfully
        if goal == nodeCur[0] :
            return get_path(explored)
        
        for node_child in graph[nodeCur[0]] :
            if(visited[node_child] == V.NOT_VISITED) :
                 queueBfs.put((node_child, nodeCur[0]))
    return None # failure
  
def DFS_Algorithm(node, path, visited, goal, graph):
    #path : save road
    #node : include nodecur, parent_node
    visited[node[0]] = V.VISITED
    #save road
    path.append((node[0], node[1]))
    
    if goal == node[0] :
        return True
    for node_child in graph[node[0]] :
        if visited[node_child] == V.NOT_VISITED :
            if DFS_Algorithm((node_child, node[0]), path, visited, goal, graph) : 
                return True
    return False

def search_DFS(graph, start, goal) :
    path = []
    visited = dict()
    for node in graph :
        visited[node] = V.NOT_VISITED #init value for node
        
    if not DFS_Algorithm((start, None), path, visited, goal, graph) :
        return None #failure
    
    return get_path(path)


def get_path(explored):
    parent_table = dict()
    for node in explored:
        parent_table[node[0]] = node[1]

    state, parent_state = explored[-1][0], explored[-1][1]
    path = deque([state])
    while parent_state is not None:
        state = parent_state
        parent_state = parent_table[state]
        path.appendleft(state)

    return list(path)

def heuristic(state, goal):      # Manhattan
    return int(abs(state[0] - goal[0]) + abs(state[1] - goal[1]))
