from enum import Enum
import random

class CState(Enum):
    FOOD = 2
    GHOST = 3
    PACMAN = 4
    EMPTY = 0
    WALL = 1


class Cell:
    def __init__(self, pos, state):
        self.pos = pos
        self.heuristic = 0
        self.visited = 0
        self.state = state


    def exist_food(self):
        return CState.FOOD in self.state


    def exist_ghost(self):
        return CState.GHOST in self.state


    def reset_heuristic(self):
        self.heuristic = 0


    def food_ate(self):
        self.state.remove(CState.FOOD)


    def ghost_leave(self):
        self.state.remove(CState.GHOST)


    def ghost_come(self):
        self.state.append(CState.GHOST)


    def pacman_leave(self):
        self.state.remove(CState.PACMAN)


    def pacman_come(self):
        self.state.append(CState.PACMAN)

        if CState.FOOD in self.state:
            self.state.remove(CState.FOOD)

        self.visited += 1


    def objective_function(self):
        return self.heuristic - (self.visited)


def calc_heuristic(graph_map, updated, start, cur, max_depth):
    updated.append(cur.pos)

    if max_depth <= 0:
        return
    if cur.visited > 10: 
        cur.heuristic -= 5*cur.visited
    for child in graph_map[cur]:
        if child.pos not in updated:
            sub_updated = []
            if child.exist_food():
                update_heuristic( graph_map, sub_updated, start, child, 2, "food")

            sub_updated = []
            sub_updated = []
            if child.exist_ghost():
                update_heuristic( graph_map, sub_updated, start, child, 2, "ghost")

            calc_heuristic( graph_map, updated.copy(), start, child, max_depth - 1)
    cur.heuristic += len(graph_map[cur])-1

def clear_heuristic(graph_map, updated, cur, max_depth):
    updated.append(cur.pos)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.pos not in updated:
            child.reset_heuristic()
            clear_heuristic( graph_map, updated.copy(), child, max_depth - 1)


def update_heuristic( graph_map, updated, start, cur, max_depth, cell_type):
    updated.append(cur.pos)

    if max_depth < 0:
        return

    if cur.pos == start.pos:
        return

    if cell_type == "food":
        food = 0
        if max_depth == 2: food = 40
        if max_depth == 1: food = 20
        if max_depth == 0: food = 5
        cur.heuristic += food

    if cell_type == "ghost":
        ghost = 0
        if max_depth == 2: ghost = float("-inf")
        if max_depth == 1: ghost = -1000 #float("-inf")'''
        if max_depth == 0: ghost = -40
        cur.heuristic += ghost

    for child in graph_map[cur]:
        if child.pos not in updated:
            update_heuristic( graph_map, updated.copy(), start, child, max_depth - 1, cell_type)


def local_search( graph_map, pacman):
    updated = [] 
    clear_heuristic( graph_map, updated, pacman, 3)

    updated = []
    calc_heuristic( graph_map, updated, pacman, pacman, 3)

    max_f = float("-inf")
    next_step = None

    for child in graph_map[pacman]:
        if max_f < child.objective_function():
            max_f = child.objective_function()
            next_step = child

    return next_step

def is_dead(pacman, ghost_list):
    if pacman in ghost_list:
        return True
    return False

def min_value(graph_map, ghost_list, food_list, score, cur, max_depth):    
    if max_depth <= 0 or len(graph_map[cur]) == 0:
        return score  
    if is_dead(cur, ghost_list):
        return score-500
    score -=  1 
    if cur.visited>15:
        return -1000
    if cur in food_list:
        score += 20
        food_list.remove(cur)
        
    for i in range(len(ghost_list)):
        distance = [max_value(graph_map, score, child, cur, max_depth) for child in graph_map[ghost_list[i]]]
        ghost_list[i] = graph_map[ghost_list[i]][distance.index(min(distance))]
    if is_dead(cur, ghost_list):
        return score-500 
    return max([min_value(
        graph_map, ghost_list.copy(), food_list.copy(),score, child, max_depth-1) for child in graph_map[cur]])

def max_value(graph_map, score, child, cur, max_depth):
    if max_depth <= 0 or len(graph_map[cur]) == 0:
        return score                             
    return abs(child.pos[0]- cur.pos[0]) + abs(child.pos[1]- cur.pos[1])
  
def minimax(graph_map, pacman_pos, ghost_list, food_list):
    max_f = float("-inf")
    next_step = []
    child_value = {}

    for child in graph_map[pacman_pos]: 
        score = 0
        child_value[child] = min_value(graph_map, ghost_list.copy(), food_list.copy(), score, child, 3)
        if max_f < child_value[child]:
            max_f = child_value[child]
    for child in graph_map[pacman_pos]:
        if max_f == child_value[child]:
            next_step.append(child)
    return random.choice(next_step)