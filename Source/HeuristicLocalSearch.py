from enum import Enum
import copy

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
        return self.heuristic - self.visited

def calc_heuristic(cells, graph_map, updated, start, cur, max_depth):
    updated.append(cur.pos)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.pos not in updated:

            sub_updated = []
            if child.exist_food():
                update_heuristic(cells, graph_map, sub_updated, start, child, 2, "food")

            sub_updated = []
            if child.exist_ghost():
                update_heuristic(cells, graph_map, sub_updated, start, child, 2, "ghost")

            calc_heuristic(cells, graph_map, updated.copy(), start, child, max_depth - 1)

    cur.heuristic -= cur.visited if (cur.visited<20) else float("inf")


def clear_heuristic(cells, graph_map, updated, cur, max_depth):
    updated.append(cur.pos)

    if max_depth <= 0:
        return

    for child in graph_map[cur]:
        if child.pos not in updated:
            child.reset_heuristic()

            clear_heuristic(cells, graph_map, updated.copy(), child, max_depth - 1)


def update_heuristic(cells, graph_map, updated, start, cur, max_depth, cell_type):
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
        if max_depth == 1: ghost = float("-inf")
        if max_depth == 0: ghost = -10
        cur.heuristic += ghost

    for child in graph_map[cur]:
        if child.pos not in updated:
            update_heuristic(cells, graph_map, updated.copy(), start, child, max_depth - 1, cell_type)


def local_search(cells, graph_map, pacman_pos):
    updated = [] 
    clear_heuristic(cells, graph_map, updated, pacman_pos, 3)

    updated = []
    calc_heuristic(cells, graph_map, updated, pacman_pos, pacman_pos, 3)

    max_f = float("-inf")
    next_step = None

    for child in graph_map[pacman_pos]:
        if max_f < child.objective_function():
            max_f = child.objective_function()
            next_step = child

    return next_step
    
'''def is_through_ghost(pacman_pos, ghost_cells):
    for ghost in ghost_cells:
        if pacman_pos.pos == ghost.pos:
            return True    
    return False
def max_search(ghost_cells, graph_map, pacman, pacman_last_pos, score, depth, alpha, beta):
 
    if depth == 3 or is_through_ghost(pacman_pos, ghost_cells):
        return alpha-1
    option = []
    for child in graph_map[pacman_pos]:
        for ghost in ghost_cells:
            if not (child.pos == ghost.pos):
                option.append(child)
    if not option:
        return alpha
    if pacman_last_pos in option:
        option.remove(pacman_last_pos)
    best_score =  float("-inf")
    for i in option:
        best_score= max(best_score, min_search(ghost_cells, graph_map, i, pacman, depth, alpha, beta))
        if (best_score>beta):
            return best_score
        alpha = max(alpha, best_score)
    return best_score


def min_search(ghost_cells, graph_cells, pacman_pos, pacman_last_pos, depth, alpha, beta):
    for i in ghost_cells:
        i.
    if game_state.get_num_agents() == 1:
        return 0

    # No Legal actions.
    if (len(game_state.get_legal_actions(agent_index)) == 0):
        return score_evaluation_func(game_state)

    action_value = float('inf')
    for action in game_state.get_legal_actions(agent_index):
        if (agent_index < game_state.get_num_agents() - 1):
            action_value = min(action_value, self.Min_Value(game_state.generate_successor(
                agent_index, action), agent_index + 1, depth, alpha, beta))
        else:  # the last ghost HERE
            action_value = min(action_value, self.Max_Value(
                game_state.generate_successor(agent_index, action), depth + 1, alpha, beta))

        if (action_value < alpha):
            return action_value
        beta = min(beta, action_value)
    return action_value
def minimax_search(ghost_cells, graph_map, pacman_pos):
    depth = 3
    alpha = float('-inf')  # max best option on path to root
    beta = float('inf')  # min best option on path to root

    action_value = float('-inf')
    max_action = None
    random_max = []
    for action in graph_map[pacman_pos]:  # get action of pacman
        action_value = min_search(copy.deepcopy(ghost_cells), graph_cells, action, pacman_pos, 0, alpha, beta)
        if (alpha < action_value):
            alpha = action_value
            max_action = action
            random_max.clear()
            random_max.append((action,  action_value)
            )
        elif alpha == action_value:
            random_max.append(
                (action,  action_value)
                )
        if len(random_max) > 0:
            (kc, kv) = random.choice(random_max)
            return kc
        return max_action'''

