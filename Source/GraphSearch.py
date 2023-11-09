import queue
import enum
from collections import deque

class V(enum.Enum):
    NOT_VISITED = 0     # state is not visited yet
    VISITED = 2        # state is explored already


def search_A(graph, start, goal):
    min_distance = dict()
    maxValue = int(10000000)
    for state in graph:
        min_distance[state] = maxValue

    node = (heuristic(start, goal), start, None)  
    frontier = queue.PriorityQueue()
    explored = [] # path
    min_distance[start] = heuristic(start, goal) 

    frontier.put(node)

    while frontier.queue:
        nodeFirst = frontier.get()
        
        if nodeFirst[0] > min_distance[nodeFirst[1]]:
            continue # skip 
        
        explored.append((nodeFirst[1], nodeFirst[2])) # add to path 
        if nodeFirst[1] == goal:      # if done
            return get_path(explored)   
        for child_state in graph[nodeFirst[1]]: # loop for adjacent list
            h_score = heuristic(nodeFirst[1], goal)
            h_child_score = heuristic(child_state, goal)
            prev_distance = nodeFirst[0] - h_score
            f_score = prev_distance + 1 + h_child_score
            if min_distance[child_state] > f_score:
                min_distance[child_state] = f_score
                frontier.put((min_distance[child_state], child_state, nodeFirst[1])) 
    return None   


def search_BFS(graph, start, goal) :
    visited = dict()
    for state in graph :
        visited[state] = V.NOT_VISITED # init
    queueBfs = queue.Queue()
    node  = (start, None)
    queueBfs.put(node)
    explored = [] # path
    
    while not queueBfs.empty():
        nodeCur = queueBfs.get()
        # already visited
        visited[nodeCur[0]] = V.VISITED
        # add to path
        explored.append((nodeCur[0], nodeCur[1]))
        
        # if done
        if goal == nodeCur[0] :
            return get_path(explored)
        
        for node_child in graph[nodeCur[0]] :
            if(visited[node_child] == V.NOT_VISITED) :
                 queueBfs.put((node_child, nodeCur[0]))
    return None
  
def DFS_Algorithm(node, path, visited, goal, graph):
    visited[node[0]] = V.VISITED
    # add to path
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
        visited[node] = V.NOT_VISITED # init
        
    if not DFS_Algorithm((start, None), path, visited, goal, graph) :
        return None
    
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

def heuristic(state, goal):      # Manhattan Distance
    return int(abs(state[0] - goal[0]) + abs(state[1] - goal[1]))
