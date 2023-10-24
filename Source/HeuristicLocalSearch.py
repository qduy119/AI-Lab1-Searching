from enum import Enum


class CState(Enum):
    FOOD = 2
    GHOST = 3
    PACMAN = 4


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
        return self.heuristic - self.visited


def calc_heuristic(cells, graph_map, remembered, start, cur, max_depth):
    remembered.append(cur.pos)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.pos not in remembered:

            sub_remembered = []
            if child.exist_food():
                update_heuristic(cells, graph_map, sub_remembered, start, child, 2, "food")

            sub_remembered = []
            if child.exist_ghost():
                update_heuristic(cells, graph_map, sub_remembered, start, child, 2, "ghost")

            calc_heuristic(cells, graph_map, remembered.copy(), start, child, max_depth - 1)

    cur.heuristic -= cur.visited


def clear_heuristic(cells, graph_map, remembered, cur, max_depth):
    remembered.append(cur.pos)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.pos not in remembered:
            child.reset_heuristic()

            clear_heuristic(cells, graph_map, remembered.copy(), child, max_depth - 1)


def update_heuristic(cells, graph_map, remembered, start, cur, max_depth, cell_type):
    remembered.append(cur.pos)

    if max_depth < 0:
        return

    if cur.pos == start.pos:
        return

    if cell_type == "food":
        food = 0
        if max_depth == 2: food = 35
        if max_depth == 1: food = 10
        if max_depth == 0: food = 5
        cur.heuristic += food

    if cell_type == "ghost":
        ghost = 0
        if max_depth == 2: ghost = float("-inf")
        if max_depth == 1: ghost = float("-inf")
        if max_depth == 0: ghost = -100
        cur.heuristic += ghost

    for child in graph_map[cur]:
        if child.pos not in remembered:
            update_heuristic(cells, graph_map, remembered.copy(), start, child, max_depth - 1, cell_type)


def local_search(cells, graph_map, pacman_pos):
    remembered = [] 
    clear_heuristic(cells, graph_map, remembered, pacman_pos, 3)

    remembered = []
    calc_heuristic(cells, graph_map, remembered, pacman_pos, pacman_pos, 3)

    max_f = float("-inf")
    next_step = None

    for child in graph_map[pacman_pos]:
        if max_f < child.objective_function():
            max_f = child.objective_function()
            next_step = child

    return next_step
