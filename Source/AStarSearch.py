import queue
import enum
from collections import deque
from tkinter.tix import INTEGER
import sys

class V(enum.Enum):
    NOT_VISITED = 0     # state is not visited yet
    FRONTIER = 1        # state is in frontier
    EXPLORED = 2        # state is explored already


def search(graph, start, goal):
    min_distance = dict()
    maxValue = int(999999)
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
            h_child_state = heuristic(child_state, goal)
            manhattan = nodeFirst[0] - h_state + 1 + h_child_state
            if min_distance[child_state] > manhattan:
                min_distance[child_state] = manhattan
                frontier.put((min_distance[child_state], child_state, nodeFirst[1]))
                
    return None     # failure


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
